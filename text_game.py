import random
import pickle
import os
import http.server as server
import urllib.parse as parse
import text_game
import time
import copy
from item import *
from monster import *
from player import *
from effects import *

class BattleComplete(Exception):
    pass

class GameHTTPRequestHandler(server.BaseHTTPRequestHandler):

    def do_GET(self):
        global g
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        #print(parse.parse_qs(parse.urlparse(self.path).query).get("var"))
        #self.wfile.write(b'Hello world')
        data = parse.parse_qs(parse.urlparse(self.path).query).get("data")
        send = g.handle(data[0])
        if send:
            self.wfile.write(send.encode())
        return

    def log_request(self, code=None, size=None):
        print('Request')

    def log_message(self, format, *args):
        print('Message')


class Battle:

    def __init__(self, party, difficulty):
        self.party = party
        for player in self.party:
            player.config_for_new_battle()
        self.difficulty = difficulty
        avg_power = sum([member.calculate_power() for member in party])/len(party)
        self.monster = Monster(difficulty, "", party)#, power = round(avg_power))
        self.battle_lost = False
        self.battle_won = False

    def newCommand(self, command): # thread_id, player_id, Move, ... args
        for member in self.party:
            if command[1] == member.name:
                player = member
        if command[2] == "get-stats":
            return "@@%s@@%s" % (player.name, player.getStats())
        elif command[2] == "get-monster":
            return "@@%s@@%s" % (player.name, self.monster.toString())
        elif command[2] == "get-health":
            return "@@%s@@Health: %d/%d" % (player.name, player.current_health, player.health)
        elif command[2] == "get-effects":
            send = "@@%s@@" % player.name
            if len(player.effects) == 0:
                send += "You currently have no effects on you.\n"
            for effect in player.effects:
                send += str(effect) + "\n"
            return send[:-1]
        elif command[2] == "get-equip":
            send = "@@%s@@" % player.name
            if len(command) > 3 and command[3]:
                send += player.get_equip(command[3])
            else:
                send += player.get_equip()
            return send
        for move in player.moves:
            if move.name == command[2]:
                player.next_move = move
                if len(command) > 3: # the command has arguments
                    player.set_args(*command[3:])
                return ""
        return "Move " + command[2] + " not found."


    def nextTurn(self):
        tmp_list = [member for member in self.party]+[self.monster] # Sorting by speed
        tmp_list.sort(key=lambda x: x.get_speed(), reverse=True)
        log = ""
        for character in tmp_list:
            skip_player_turn = False
            for effect in character.effects:
                if not effect.active:
                    continue
                cont, msg = effect.on_start_turn(self, character)
                log += msg
                if cont == False:
                    skip_player_turn = True
            if character.fallen:
                skip_player_turn = True
            if skip_player_turn:
                continue
            log += character.handle(self) + "\n"
            for effect in character.effects:
                if not effect.active:
                    continue
                log += effect.on_end_turn(self, character)
            for character in tmp_list:
                if character.current_health <= 0:
                    if type(character) == Monster:
                        for effect in character.effects:
                            if not effect.active:
                                continue
                            if not effect.on_death(self, character):
                                break
                        else:
                            log += character.name + " has fallen.\nVictory!\n"
                            character.fallen = True
                            self.battle_won = True
                            return log
                    elif type(character) == Player:
                        for effect in character.effects:
                            if not effect.active:
                                continue
                            if not effect.on_death(self, character):
                                break
                        else:
                            if character not in self.getDeadPlayers(): # Just died
                                log += character.name + " has fallen.\n"
                                character.fallen = True
                                if len(self.getDeadPlayers()) == len(self.party):
                                    self.battle_lost = True
                                    log += "All members of your party have fallen. Game Over"
                                    return log
        return log

    def getDeadPlayers(self):
        dead_players = []
        for member in self.party:
            if member.fallen:
                dead_players.append(member)
        return dead_players

    def handleFinish(self):
        send = ""
        if self.battle_won:
            for member in self.party:
                if member not in self.getDeadPlayers():
                    tmp_item = Item(self.monster.power, self.difficulty)
                    member.drop = tmp_item
                    gained_experience = member.give_experience(EXPERIENCE_PER_BATTLE)
                    send += "@@" + member.name + "@@You gained %d experience.\n========================\n" %gained_experience
                    if member.is_level_up():
                        send += member.level_up() + "\n========================\n"
                    send += "You found: " + tmp_item.name + "\n" + tmp_item.getStats()
                    send += "\nTo equip type \\yes, to drop the item type \\no. Note starting a new game will remove your drop.\n========================"
                else:
                    send += "@@" + member.name
                    send += "@@" + "Your character is dead."
        if self.battle_lost:
            for member in self.party:
                send += "@@" + member.name
                send += "@@" + "Your character is dead."
        return send


class Game:

    def __init__(self):
        # name, attack, defense, speed, health, slot, other
        self.battles = {}
        self.players = {}
        if os.path.exists("player.data"):
            self.load()
        self.return_data = ""

    def handle(self, command):
        if command != "":
            print(command)
            self.return_data = ""
            self.return_data = self.inputCommand(command.split(' '))
            return self.return_data

    def inputCommand(self, command):
        #================== STATUS CHECK OF PARTY ======================#
        try:
            cur_party = self._get_party(command)
            if cur_party: # if current batttle exists
                send = self.handleBattle(command)
                if cur_party.battle_won or cur_party.battle_lost:
                    raise BattleComplete
                return send
        except KeyError:
            pass
        except BattleComplete:
            send += self._get_party(command).handleFinish()
            for player in self._get_party(command).getDeadPlayers():
                self.removePlayer(player)
            send += "@@zuckerbot@@end " + command[0]
            self._remove_party(command)
            return send

        #================== Commands ======================#
        if command[2] == "start-game":
            try:
                if command[3] not in ("normal", "hard", "boss"):
                    return "Please choose a difficulty: normal, hard, boss."
            except IndexError:
                return "Please choose a difficulty: normal, hard, boss."
            self.battles[command[0]] = []
            tmp_party = []
            for name in command[4:]:
                if self.players.get(name) == None:
                    self.players[name] = Player(name)
                tmp_party.append(self.players[name])
            if command[3] == "normal": difficulty = 1
            elif command[3] == "hard": difficulty = 2
            elif command[3] == "boss": difficulty = 3
            self.battles[command[0]] = Battle(tmp_party, difficulty)
            send = "Battle commencing!...\n"+self.battles[command[0]].monster.toString()
            for member in tmp_party:
                send += "@@" + member.name
                send += "@@" + member.getStats()
            return send
        elif command[2] == "stop-game":
            return "You are not in a game! Why are you trying to stop it!"
        elif command[0] == command[1]: # Player chat
            if command[2] == "yes":
                if self.players[command[1]].drop != None:
                    successful = False
                    if len(command) > 3:
                        successful = self.players[command[1]].equip(self.players[command[1]].drop, command[3])
                    else:
                        successful = self.players[command[1]].equip(self.players[command[1]].drop)
                    if successful:
                        self.players[command[1]].drop = None # Remove the item from drop
                        send = "Successfully equiped your item.@@zuckerbot@@end" + command[0]
                    else:
                        send = "Equip unsuccessful. Some types of items (extra and hand) require an additional argument after yes indicted which slot to add into. Example: /yes hand1 to equip to first hand slot."
                    return send
            elif command[2] == "no":
                if self.players[command[1]].drop != None:
                    self.players[command[1]].drop = None # Remove the item from drop
                    return "Item was dropped.@@zuckerbot@@end" + command[0]
            else:
                return "Command doesn't exist. Please type in help for information."
        else:
            return "Command doesn't exist. Please type in help for information."

    def handleBattle(self, command):
        cur_party = self._get_party(command)
        if command[2] == "stop-game":
            self._remove_party(command)
            return "Game session ended.@@zuckerbot@@end" + command[0]
        elif command[2] == "next":
            return cur_party.nextTurn()
        else:
            return cur_party.newCommand(command)

    def newPlayer(self, name):
        if self.players.get(name) == None:
            self.players[name] = Player(name)

    def clearPlayers(self):
        self.players = {}

    def removePlayer(self, player):
        self.players.pop(player.name)

    def _get_party(self, command):
        """Returns the current party being used"""
        return self.battles[command[0]]

    def _remove_party(self, command):
        """Removes the current party"""
        self.battles.pop(command[0])

    def save(self):
        with open("player.data", "wb") as file:
            pickle.dump(self.players, file)

    def load(self,):
        with open("player.data", "rb") as file:
            try:
                self.players = pickle.load(file)
            except EOFError: # Empty player list is made
                self.players = {}

    def quit(self):
        self.save()

if __name__ == "__main__":
    g = Game()
    PORT = 34567
    handler = GameHTTPRequestHandler
    try:
        httpd = server.HTTPServer(("localhost", PORT), handler)
        print('Started http server')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        g.quit()
        httpd.socket.close()
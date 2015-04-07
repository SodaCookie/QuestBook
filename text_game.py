import random
import pickle
import http.server as server
import urllib.parse as parse
import text_game
import time
import copy
import effects
import moves
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
        self.difficulty = difficulty
        self.monster = Monster(difficulty, "", party)
        self.battle_lost = False
        self.battle_won = False

    def newCommand(self, command): # ,thread_id, player_id, Move, ... args
        for member in self.party:
            if command[1] == member.name:
                player = member
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
                cont, msg = effect.on_start_turn(self, character)
                log += msg
                if cont == False:
                    skip_player_turn = True
            if skip_player_turn:
                continue
            log += character.handle(self) + "\n"
            for effect in character.effects:
                log += effect.on_end_turn(self, character)
            for character in tmp_list:
                if character.current_health <= 0:
                    if type(character) == Monster:
                        for effect in character.effects:
                            if not effect.on_death(self, character):
                                break
                        else:
                            log += character.name + " has fallen.\nVictory!\n"
                            self.battle_won = True
                    elif type(character) == Player:
                        for effect in character.effects:
                            if not effect.on_death(self, character):
                                break
                        else:
                            log += character.name + " has fallen.\n"
                            character.add_effect(Fallen(999))
                            if len(self.getDeadPlayers()) == len(self.party):
                                self.battle_lost = True
                                log += "All members of your party have fallen. Game Over"
                                return log
        return log

    def getDeadPlayers(self):
        dead_players = []
        for member in self.party:
            for effect in member.effects:
                if effect.name == "fallen":
                    dead_players.append(member)
        return dead_players

    def handleFinish(self):
        send = ""
        if self.battle_won:
            for member in self.party:
                if member not in self.getDeadPlayers():
                    tmp_item = Item(50, self.difficulty)
                    send += "@@" + member.name
                    send += "@@" + "You found: " + tmp_item.name + "\n" + tmp_item.getStats()
        if self.battle_lost:
            pass
        return send


class Game:

    def __init__(self):
        # name, attack, defense, speed, health, slot, other
        self.battles = {}
        self.players = {}
##        with open("players.dat", "rb") as f:
##            self.players = pickle.load(f)

    def handle(self, command):
        if command != "":
            print(command)
            return self.inputCommand(command.split(' '))

    def inputCommand(self, command):

        #================== STATUS CHECK OF PARTY ======================#
        try:
            cur_party = self._get_party(command)
            if cur_party: # if current batttle exists
                send = self.handleBattle(command)
                if self._get_party(command).battle_won or self._get_party(command).battle_lost:
                    raise BattleComplete
                return send
        except KeyError:
            pass
        except BattleComplete:
            send += self._get_party(command).handleFinish()
            for player in self._get_party(command).getDeadPlayers():
                self.removePlayer(player)
                send += "@@" + player.name
                send += "@@" + "Your character is dead."
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
                tmp_party.append(copy.deepcopy(self.players[name]))
            if command[3] == "normal": difficulty = 1
            elif command[3] == "hard": difficulty = 2
            elif command[3] == "boss": difficulty = 3
            self.battles[command[0]] = Battle(tmp_party, difficulty)
            send = "Battle commencing!...\n"+self.battles[command[1]].monster.toString()
            for member in tmp_party:
                send += "@@" + member.name
                send += "@@" + member.getStats()
            return send

        elif command[2] == "stop-game":
            return "You are not in a game! Why are you trying to stop it!"
        elif command[2] == "help":
            pass
        else:
            return "Command doesn't exist. Please type in help for information."

    def handleBattle(self, command):
        cur_party = self._get_party(command)
        if command[2] == "stop-game":
            self._remove_party(command)
            return "Game session ended."
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

    def quitGame(self):
        with open("players.dat", "wb") as f:
            pickle.dump(self.players, f)

if __name__ == "__main__":
    g = Game()
    PORT = 34567
    handler = GameHTTPRequestHandler
    try:
        httpd = server.HTTPServer(("", PORT), handler)
        print('Started http server')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        g.quitGame()
        httpd.socket.close()
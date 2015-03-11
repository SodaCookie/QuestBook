import random
import pickle
import http.server as server
import urllib.parse as parse
import text_game
import time
import copy
import effects

POWER_BASE = 2 # Used to measure the difficulty of monsters of different difficulty: 20% more stats
ATTACK_HEURISTIC = 1 # Used to gauge how useful attack is as a stat
DEFENSE_HEURISTIC = 1 # Used to gauge how useful defense is as a stat
HEALTH_HEURISTIC = 0.2 # Used to gauge how useful health is as a stat
SPEED_HEURISTIC = 5 # Used to gauge how useful speed is as a stat
MAGIC_HEURISTIC = 0.5  # Used to gauge how useful magic is as a stat

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

class Monster:

    def __init__(self, difficulty = 1, monster = "", power=0): # ELITE AND BOSS MONSTER HAVE GUARENTEED ABILITES, ABILTY IS BASED ON MAGIC
        self.difficulty = difficulty
        self.effects = []
        self.name = ""
        self.monster = monster
        self.monstertype = ""
        self.attack = 0
        self.defense = 0
        self.magic = 0
        self.current_health = 100
        self.health = 100
        self.speed = 10
        self.abilities = [] # List of ids that give abilities
        with open("prefix.txt", "r") as f:
            self.prefix = f.read().split("\n")
        with open("monster.txt", "r") as f:
            self.monster = f.read().split("\n")
        with open("suffix.txt", "r") as f:
            self.suffix = f.read().split("\n")
        self.generateName()
        self.generateStats(power)


    def generateStats(self, power):
        """Generates stats based on the power level of the players"""
        power = power*POWER_BASE**(self.difficulty-1) # power is used to generate points for the monster
        r1, r2, r3, r4, r5, r6 = [random.randint(0,100) for i in range(6)]
        s = r1 + r2 + r3 + r4 + r5 + r6 # Divide the power into 6 random parts

        self.attack = round(power*r1/s/ATTACK_HEURISTIC)
        self.defense = round(power*r2/s/DEFENSE_HEURISTIC)
        self.health = round(power*r3/s/HEALTH_HEURISTIC)
        self.speed = round(power*r4/s/SPEED_HEURISTIC)
        self.magic = round(power*r5/s/MAGIC_HEURISTIC)
        self.current_health = self.health

    def generateName(self):
        choices = {}
        if self.monstertype == "":
            choices["monster"] = random.choice(self.monster)
        else:
            # Placeholder. If specified monster type
            choices["monster"] = self.monster
        if self.difficulty >= 2:
            choices["prefix"] = random.choice(self.prefix)
        if self.difficulty >= 3:
            choices["suffix"] = random.choice(self.suffix)

        if self.difficulty == 1:
            self.name = "%(monster)s" % (choices)
        elif self.difficulty == 2:
            self.name = "%(prefix)s %(monster)s" % (choices)
        elif self.difficulty == 3:
            self.name = "%(prefix)s %(monster)s of %(suffix)s" % (choices)

    def toString(self):
        return 'Name: %s\nAttack: %d\nDefense: %d\nHealth: %d\nSpeed: %d'\
     % (self.name, self.attack, self.defense, self.health, self.speed)

class Player:

    def __init__(self, name):
        self.name = name
        self.effects = []
        self.attack = 5
        self.defense = 0
        self.magic = 0
        self.current_health = 100
        self.health = 100
        self.speed = 10

        self.experience = 0
        self.level = 1

        self.equipment = {}
        self.equipment["hand1"] = Item(generate=False)
        self.equipment["hand2"] = Item(generate=False)
        self.equipment["body"] = Item(generate=False)
        self.equipment["legs"] = Item(generate=False)
        self.equipment["feet"] = Item(generate=False)
        self.equipment["arms"] = Item(generate=False)
        self.equipment["head"] = Item(generate=False)
        self.equipment["extra1"] = Item(generate=False)
        self.equipment["extra2"] = Item(generate=False)

    def update(self):
        for item in self.equipment.values():
            self.attack += item.attack
            self.defense += item.defense
            self.health += item.health
            self.speed += item.speed
            self.magic += item.magic

    def equip(item, slot):
        if self.equipment.get(slot) and self.equipment[slot] != "":
            equipable = False
            if item.slot == "any":
                equipable = True
            elif item.slot == "hand" and (slot == "hand1" or slot == "hand2"):
                equipable == True
            elif item.slot == "body" and slot == "body":
                equipable == True
            elif item.slot == "legs" and slot == "legs":
                equipable == True
            elif item.slot == "feet" and slot == "feet":
                equipable == True
            elif item.slot == "arms" and slot == "arms":
                equipable == True
            elif item.slot == "head" and slot == "head":
                equipable == True
            elif item.slot == "extra" and (slot == "extra1" or slot == "extra2"):
                equipable == True
            if equipable:
                self.equipment[slot] = item

    def handlePlayerTurn(self):
        pass

    def getStats(self):
        return ' | EXP: %d | LVL %d\n========================\nAttack: %d\nDefense: %d\nHealth: %d\\%d\nSpeed: %d\nMagic: %d'\
     % (self.experience, self.level, self.attack, self.defense, self.current_health, self.health, self.speed, self.magic)


class Item:

    def __init__(self, power=0, difficulty=1, generate=True):
        """Generate indicates whether or not you want to auto generate an item"""
        self.name = "None" # Negative weight measn that the items has a chance to decreases stats
        self.power = power
        self.difficulty = difficulty
        self.rarity = "normal"
        self.paradigm = "" # The kind of item, Attack, Defense, Support, Magical
        self.attack = 0
        self.attack_weight = 1 # Used to help direct the chance of higher attack stats
        self.defense = 0
        self.defense_weight = 1 # Used to help direct the chance of higher defense stats
        self.speed = 0
        self.speed_weight = 1 # Used to help direct the chance of higher speed stats
        self.health = 0
        self.health_weight = 1 # Used to help direct the chance of higher health stats
        self.magic = 0
        self.magic_weight = 1 # Used to help direct the chance of higher magic stats
        self.slot = ""
        self.ability_weight = 1 # Used to help direct the chance of higher ability values
        self.ability = []
        self.other = 0
        self.base = 1 # used to amp total stats up and down (ie rusty vs shiny)
        self.chosen_item = ""
        self.chosen_prefix = ""
        self.chosen_presuffix = ""
        self.chosen_suffix = ""
        if generate:
            self.generateName()
            self.generateStats()

    def generateStats(self):
        if self.rarity == "legendary":
            self.power = self.power*POWER_BASE**3
        elif self.rarity == "epic":
            self.power = self.power*POWER_BASE**2
        elif self.rarity == "rare":
            self.power = self.power*POWER_BASE
        elif self.rarity == "normal":
            pass
        self.power = self.power*self.base

        if self.chosen_item in ["Sword", "Dagger", "Axe", "Greatsword", "Spear", "Staff", "Wand", "Spellbook", "Crystal", "Doll", "Shield", "Tower Shield"]:
            self.slot = "hand"
        elif self.chosen_item in ["Armor"]:
            self.slot = "body"
        elif self.chosen_item in ["Pants", "Leggings"]:
            self.slot = "legs"
        elif self.chosen_item in ["Boots"]:
            self.slot = "feet"
        elif self.chosen_item in ["Gloves"]:
            self.slot = "arms"
        elif self.chosen_item in ["Helm"]:
            self.slot = "head"
        elif self.chosen_item in ["Necklace", "Ring", "Earring"]:
            self.slot = "extra"

        if self.paradigm == "attack":
            self.attack_weight = 2
            self.defense_weight = 0.1
            self.health_weight = 0.1
            self.speed_weight = 0.1
            self.magic_weight = 0.1
            self.ability_weight = 1
        elif self.paradigm == "defense":
            self.attack_weight = 0.1
            self.defense_weight = 1.5
            self.health_weight = 1.5
            self.speed_weight = 0.1
            self.magic_weight = 0.1
            self.ability_weight = 1
        elif self.paradigm == "support":
            self.attack_weight = 0.1
            self.defense_weight = 1
            self.health_weight = 1
            self.speed_weight = 1.1
            self.magic_weight = 1.1
            self.ability_weight = 2
        elif self.paradigm == "magical":
            self.attack_weight = 0.5
            self.defense_weight = 0.2
            self.health_weight = 0.2
            self.speed_weight = 1
            self.magic_weight = 2
            self.ability_weight = 2

        # FINISH ADD STAT CHANGES IN WEIGHT DEPENDING ON ITEM TYPE AND PREFFIXES

        r1, r2, r3, r4, r5, r6 = [random.randint(0,100) for i in range(6)]
        r1 = r1 * self.attack_weight
        r2 = r2 * self.defense_weight
        r3 = r3 * self.speed_weight
        r4 = r4 * self.health_weight
        r5 = r5 * self.magic_weight
        r6 = r6 * self.ability_weight
        s = r1 + r2 + r3 + r4 + r5 + r6 # Divide the power into 6 random parts

        self.attack = round(self.power*r1/s/ATTACK_HEURISTIC)
        self.defense = round(self.power*r2/s/DEFENSE_HEURISTIC)
        self.health = round(self.power*r3/s/HEALTH_HEURISTIC)
        self.speed = round(self.power*r4/s/SPEED_HEURISTIC)
        self.magic = round(self.power*r5/s/MAGIC_HEURISTIC)

    def generateName(self):
        rarity_roll = random.randint(0,1000)
        if self.difficulty == 1:
            if rarity_roll > 990:
                self.rarity = "epic"
            elif rarity_roll > 900:
                self.rarity = "rare"
            else:
                self.rarity = "normal"
        elif self.difficulty == 2:
            if rarity_roll > 990:
                self.rarity = "legendary"
            elif rarity_roll > 900:
                self.rarity = "epic"
            elif rarity_roll > 500:
                self.rarity = "rare"
            else:
                self.rarity = "normal"
        elif self.difficulty == 3:
            if rarity_roll > 900:
                self.rarity = "legendary"
            elif rarity_roll > 500:
                self.rarity = "epic"
            elif rarity_roll < 1:
                self.rarity = "normal"
            else:
                self.rarity = "rare"

        self.paradigm = random.choice(("attack", "defense", "support", "magical"))

        if self.paradigm == "attack":
            items = ["Sword", "Dagger", "Axe", "Greatsword", "Spear"]
        elif self.paradigm == "defense":
            items = ["Shield", "Armor", "Gloves", "Leggings", "Helm", "Boots", "Tower Shield", "Pants"]
        elif self.paradigm == "support":
            items = ["Necklace", "Ring", "Earring"]
        elif self.paradigm == "magical":
            items = ["Staff", "Wand", "Spellbook", "Crystal", "Doll"]

        prefix = []
        presuffix = []
        suffix = []
        if self.rarity == "normal":
            prefix = ["Apprentice", "Simple", "Carved", "Worn", "Broken"]
            if self.paradigm == "magical" or self.paradigm == "support":
                prefix += ["Weak", "Acolyte", "Lesser"]
            else:
                prefix += ["Rusty", "Rusted"]
            if random.randint(0,10000) < 1:
                prefix += ["NOOB"]

        elif self.rarity == "rare":
            prefix = ["Light", "Fire", "Ice", "Lightning", "Dark", "Gilded", "Silver", "Polished", "Emerald"]
            if self.paradigm == "magical":
                prefix += ["Wizard", "Bewitching", "Magical", "Greater", "Elemental"]
            else:
                prefix += ["Hero", "Gleaming", "Steel", "Chain"]

        elif self.rarity == "epic":
            prefix = ["Solar", "Sacred", "Glacial", "Thunderous", "Shadow", "Gilded", "Golden", "Shining", "Crystal", "Forest", "Inferno", "Heavenly"]
            if self.paradigm == "magical":
                prefix += ["Master", "Bewitching", "Magical", "Greatest", "Force", "Elemental", "Necromancer"]
            else:
                prefix += ["Dragon", "Humanity", "Mythril", "Challenging"]
            suffix = ["Heroes", "Flare", "Power", "Intelligence", "Brawn", "Spellweaving", "Rest", "Tranquility"]

        elif self.rarity == "legendary":
            prefix = ["Solar", "Sacred", "Tidal", "Thunderous", "Infinity", "Abysal", "Overwhelming", "Unmovable", "Shining", "Perfect", "Nature", "Inferno", "Heavenly", "Judgement",\
                      "Earthshattering", "Hell-Forged", "Dragon Aspect", "Godly", "Temporal"]
            if self.paradigm == "magical":
                prefix += ["Masterful", "Greatest Bewitching", "Magical", "Imperial", "Ultimate", "Force", "Elemental", "Necromancer"]
            else:
                prefix += ["Dragon", "Worldly", "Runic", "Skyward", "Gravity", "Time"]
            suffix = ["Tundra", "Flare", "Power", "Intelligence", "Brawn", "Spellweaving", "Heaven", "Tranquility", "Time", "God", "Shadow", "Hell", "Space"]
            presuffix = ["Fiery", "Glacial", "Infinite", "Earthly", "Sacred", "Master", "Elemental", "Burning", "Halt", "Stop"]

        self.chosen_item = random.choice(items)
        self.name = self.chosen_item
        if prefix:
            self.chosen_prefix = random.choice(prefix)
            self.name = self.chosen_prefix + " " + self.name
        if suffix:
            self.chosen_suffix = random.choice(suffix)
            self.name = self.name + " of"
            if presuffix:
                self.chosen_presuffix = random.choice(presuffix)
                self.name = self.name + " " + self.chosen_presuffix
            self.name = self.name + " " + self.chosen_suffix

    def getStats(self):
        return 'Attack: %d\nDefense: %d\nHealth: %d\nSpeed: %d\nMagic: %d'\
     % (self.attack, self.defense, self.health, self.speed, self.magic)


class Battle:

    def __init__(self, party, difficulty):
        self.party = party
        self.difficulty = difficulty
        # Sum of attack, defense, health, magic and speed for all players
        # Then averaged out
        averageStats = 0
        for p in party:
            averageStats += p.attack + p.defense + p.health + p.magic + p.speed

        averageStats /= len(party)
        print(averageStats)
        self.monster = Monster(difficulty, "", averageStats)
        self.battle_complete = False
        self.monster = Monster(difficulty, "", 50)
        self.commands = {}
        for member in self.party:
            self.commands[member.name] = "attack"

    def newCommand(self, command, name):
        if command[0] == "attack":
            self.commands[name] = "attack"
        elif command[0] == "defend":
            self.commands[name] = "defend"

    def nextTurn(self):
        tmp_list = [member for member in self.party]+[self.monster] # Sorting by speed
        tmp_list.sort(key=lambda x: x.speed, reverse=True)
        log = ""

        for character in tmp_list:
            if type(character) == Monster:
                log += self.handleMonster(character)
            elif type(character) == Player:
                log += self.handlePlayer(character)
            for character in tmp_list:
                if character.current_health <= 0:
                    if type(character) == Monster:
                        for effect in character.effects:
                            if not effect.on_death(self, character):
                                break
                        else:
                            log += character.name + " has fallen.\nVictory!\n"
                            self.battle_complete = True
                    elif type(character) == Player:
                        for effect in character.effects:
                            if not effect.on_death(self, character):
                                break
                        else:
                            log += character.name + " has fallen.\n"

        if self.battle_complete:
            for member in self.party:
                tmp_item = Item(50, self.difficulty)
                send += "@@" + member.name
                send += "@@" + "You found: " + tmp_item.name + "\n" + tmp_item.getStats()
            return log

        for member in self.party:
            self.commands[member.name] = "attack"
        return log

    def handleMonster(self, monster):
        log = ""
        attacked_player = random.choice(self.party) # attack a player
        damage = character.attack - attacked_player.defense
        if damage <= 0:
            damage = 1
        for effect in attacked_player.effects:
            damage = effect.on_damage(self, damage)
        attacked_player.current_health -= damage
        log += attacked_player.name + " took %d damage.\n" % damage
        if attacked_player.current_health <= 0:
            log += attacked_player.name + " has fallen.\n"

        # Remove the effect after the duration is gone
        for effect in monster.effects[:]:
            effect.duration -= 1
            if effect.duration <= 0:
                player.effects.remove(effect)

        return log

    def handlePlayer(self, player):
        log = ""
        if self.commands[player.name] == "attack":
            damage = character.attack - self.monster.defense
            if damage <= 0:
                damage = 1
            for effect in self.monster.effects:
                damage = effect.on_damage(self, damage)
            self.monster.current_health -= damage
            log += self.monster.name + " took %d damage.\n" % damage
        elif self.commands[player.name] == "defend":
            if "defending" not in character.effects:
                character.effects.append(effect.Blocking(2, 0.5)) # It needs two because itll decay by one

        # Remove the effect after the duration is gone
        for effect in player.effects[:]:
            effect.duration -= 1
            if effect.duration <= 0:
                player.effects.remove(effect)

class Game:

    def __init__(self):
        # name, attack, defense, speed, health, slot, other
        self.battles = {}
        with open("players.dat", "rb") as f:
            self.players = pickle.load(f)

    def handle(self, command):
        if command != "":
            print(command)
            return self.inputCommand(command.split(' '))

    def inputCommand(self, command):

        try:
            if self.battles[command[1]].battle_complete:
                raise BattleComplete
            cur_party = self.battles[command[1]]
            print(cur_party)
            if cur_party:
                return self.handleBattle(command)
        except KeyError:
            pass
        except BattleComplete:
            self.battles[command[1]] = None # Remove the battle

        if command[0] == "start-game":
            try:
                if command[2] not in ("normal", "hard", "boss"):
                    return "Please choose a difficulty: normal, hard, boss."
            except IndexError:
                return "Please choose a difficulty: normal, hard, boss."
            self.battles[command[1]] = []
            tmp_party = []
            for name in command[3:]:
                if self.players.get(name) == None:
                    self.players[name] = Player(name)
                tmp_party.append(copy.deepcopy(self.players[name]))
            if command[2] == "normal": difficulty = 1
            elif command[2] == "hard": difficulty = 2
            elif command[2] == "boss": difficulty = 3
            self.battles[command[1]] = Battle(tmp_party, difficulty)
            send = "Battle commencing!...\n"+self.battles[command[1]].monster.toString()
            for member in tmp_party:
                send += "@@" + member.name
                send += "@@" + member.getStats()
            return send

        elif command[0] == "stop-game":
            return "You are not in a game! Why are you trying to stop it!"
        elif command[0] == "help":
            pass
        else:
            return "Command doesn't exist. Please type in help for information."

    def handleBattle(self, command):
        cur_party = self.battles[command[1]]
        if command[0] == "stop-game":
            return "Game session ended. :("
        elif command[0] == "next":
            return self.battles[command[1]].nextTurn()
        else:
            return self.battles[command[1]].newCommand(command)

    def newPlayer(self, name):
        if self.players.get(name) == None:
            self.players[name] = Player(name)

    def clearPlayers(self):
        self.players = {}

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
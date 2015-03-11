import random
import pickle

class Monster:

    def __init__(self, difficulty = 1, monster = ""):
        self.difficulty = difficulty
        self.monster = monster
        self.monstertype = ""
        self.attack = 0
        self.defense = 0
        self.health = 100
        self.speed = 10
        with open("prefix.txt", "r") as f:
            self.prefix = f.read().split("\n")
        with open("monster.txt", "r") as f:
            self.monster = f.read().split("\n")
        with open("suffix.txt", "r") as f:
            self.suffix = f.read().split("\n")

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
            return "%(monster)s" % (choices)
        elif self.difficulty == 2:
            return "%(prefix)s %(monster)s" % (choices)
        elif self.difficulty == 3:
            return "%(prefix)s %(monster)s of %(suffix)s" % (choices)


class Player:

    def __init__(self, name):
        self.name = name
        self.attack = 5
        self.defense = 0
        self.health = 100
        self.speed = 10

        self.experience = 0
        self.level = 1

        self.equipment = {}
        self.equipment["hand1"] = "fist"
        self.equipment["hand2"] = "fist"
        self.equipment["body"] = ""
        self.equipment["legs"] = ""
        self.equipment["feet"] = ""
        self.equipment["arms"] = ""
        self.equipment["head"] = ""
        self.equipment["extra1"] = ""
        self.equipment["extra2"] = ""

    def update(self):
        for item in self.equipment.values():
            self.attack += item.attack
            self.defense += item.defense
            self.health += item.health
            self.speed += item.speed

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


class Item:

    def __init__(self, stats):
        self.name = stats[0]
        self.attack = int(stats[1])
        self.defense = int(stats[2])
        self.speed = int(stats[3])
        self.health = int(stats[4])
        self.slot = stats[5]
        self.other = int(stats[6])

class Battle:

    def __init__(self, players):
        self.enemy = Monster()
        self.players = players
        self.commands = []

    def addCommand(self, command):
        # DO SOME TEXT MANIPULATION
        self.commands.append(command)

    def nextTurn(self):
        for command in self.commands:
            command = command.split(" ")
            if command[0] == "-attack":
                pass
            elif command[0] == "-ability":
                if command[1] == "ability1":
                    pass
            elif command[0] == "-defend":
                pass
        self.commands = []

class Game:

    def __init__(self):
        # name, attack, defense, speed, health, slot, other
        self.items = {}
        with open("items.txt", "r") as f:
            data = f.read()
            for item in data.split("\n"):
                stats = item.split(",")
                self.items[stats[0]] = Item(stats)
        # Players
        with open("players.dat", "rb") as f:
            self.players = pickle.load(f)

    def inputCommand(self, command):
        pass

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
    command = ""
    while command != "quit":
        pass
    g.quitGame()

##    command = ""
##    while command != "quit":
##        command = input()
##        if command != "":
##            b.addCommand(command)
##        if command == "/go":
##            b.nextTurn()
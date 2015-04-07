import random
from constants import *

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
        self.chosen_prefix = []
        self.chosen_presuffix = []
        self.chosen_suffix = []
        if generate:
            self.generate()

    def generate(self):
        # difficulty rolling for item rarity
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
        # parsing the itemtype file
        with open("itemtypes.txt", "r") as f:
            data = f.read().split("\n")
            itemtypes = []
            for line in data:
                stats = line.split(",")
                item = stats[0]
                paradigm = stats[1]
                slot = stats[2]
                base = float(stats[3])
                attack = float(stats[4])
                defense = float(stats[5])
                health = float(stats[6])
                speed = float(stats[7])
                magic = float(stats[8])
                ability = float(stats[9])
                moves = eval(stats[10]) # interprets a list
                if paradigm == self.paradigm:
                    itemtypes.append([item, paradigm, slot, base, attack, defense, health, speed, magic, ability, moves])
        # Choosing the item type of choice
        self.chosen_item = random.choice(itemtypes)
        # Naming the item
        with open("itemprefix.txt", "r") as f:
            data = f.read().split("\n")
            itemprefixes = []
            for line in data:
                stats = line.split(",")
                name = stats[0]
                rarity = stats[1]
                paradigm = stats[2]
                weapon = stats[3]
                base = float(stats[4])
                attack = float(stats[5])
                defense = float(stats[6])
                health = float(stats[7])
                speed = float(stats[8])
                magic = float(stats[9])
                ability = float(stats[10])
                moves = eval(stats[11])
                if (weapon == self.chosen_item[0] or weapon == "any") and (paradigm == self.paradigm or paradigm == "any") and rarity == self.rarity:
                    itemprefixes.append([name, rarity, paradigm, weapon, base, attack, defense, health, speed, magic, ability, moves])
        with open("itempresuffix.txt", "r") as f:
            data = f.read().split("\n")
            itempresuffixes = []
            for line in data:
                stats = line.split(",")
                name = stats[0]
                rarity = stats[1]
                paradigm = stats[2]
                weapon = stats[3]
                base = float(stats[4])
                attack = float(stats[5])
                defense = float(stats[6])
                health = float(stats[7])
                speed = float(stats[8])
                magic = float(stats[9])
                ability = float(stats[10])
                moves = eval(stats[11])
                if (weapon == self.chosen_item[0] or weapon == "any") and (paradigm == self.paradigm or paradigm == "any") and rarity == self.rarity:
                    itempresuffixes.append([name, rarity, paradigm, weapon, base, attack, defense, health, speed, magic, ability, moves])
        with open("itemsuffix.txt", "r") as f:
            data = f.read().split("\n")
            itemsuffixes = []
            for line in data:
                stats = line.split(",")
                name = stats[0]
                rarity = stats[1]
                paradigm = stats[2]
                weapon = stats[3]
                base = float(stats[4])
                attack = float(stats[5])
                defense = float(stats[6])
                health = float(stats[7])
                speed = float(stats[8])
                magic = float(stats[9])
                ability = float(stats[10])
                moves = eval(stats[11])
                if (weapon == self.chosen_item[0] or weapon == "any") and (paradigm == self.paradigm or paradigm == "any") and rarity == self.rarity:
                    itemsuffixes.append([name, rarity, paradigm, weapon, base, attack, defense, health, speed, magic, ability, moves])

        self.name = self.chosen_item[0]
        if itemprefixes: self.chosen_prefix = random.choice(itemprefixes)
        if itempresuffixes: self.chosen_presuffix = random.choice(itempresuffixes)
        if itemsuffixes: self.chosen_suffix = random.choice(itemsuffixes)
        self.base = self.chosen_item[3]
        self.attack_weight = self.chosen_item[4]
        self.defense_weight = self.chosen_item[5]
        self.health_weight = self.chosen_item[6]
        self.speed_weight = self.chosen_item[7]
        self.magic_weight = self.chosen_item[8]
        self.ability_weight = self.chosen_item[9]
        if self.chosen_prefix:
            self.name = self.chosen_prefix[0] + " " + self.name
            self.base *= self.chosen_prefix[4]
            self.attack_weight += self.chosen_prefix[5]
            self.defense_weight += self.chosen_prefix[6]
            self.health_weight += self.chosen_prefix[7]
            self.speed_weight += self.chosen_prefix[8]
            self.magic_weight += self.chosen_prefix[9]
            self.ability_weight += self.chosen_prefix[10]
        if self.chosen_presuffix:
            self.name = self.name + " of " + self.chosen_presuffix[0] + " " + self.chosen_suffix[0]
            self.base *= self.chosen_presuffix[4]
            self.attack_weight += self.chosen_presuffix[5]
            self.defense_weight += self.chosen_presuffix[6]
            self.health_weight += self.chosen_presuffix[7]
            self.speed_weight += self.chosen_presuffix[8]
            self.magic_weight += self.chosen_presuffix[9]
            self.ability_weight += self.chosen_presuffix[10]
            # Suffix weights added
            self.base *= self.chosen_suffix[4]
            self.attack_weight += self.chosen_suffix[5]
            self.defense_weight += self.chosen_suffix[6]
            self.health_weight += self.chosen_suffix[7]
            self.speed_weight += self.chosen_suffix[8]
            self.magic_weight += self.chosen_suffix[9]
            self.ability_weight += self.chosen_suffix[10]
        elif self.chosen_suffix:
            self.name = self.name + " of " + self.chosen_suffix[0]
            self.base *= self.chosen_prefix[4]
            self.attack_weight += self.chosen_suffix[5]
            self.defense_weight += self.chosen_suffix[6]
            self.health_weight += self.chosen_suffix[7]
            self.speed_weight += self.chosen_suffix[8]
            self.magic_weight += self.chosen_suffix[9]
            self.ability_weight += self.chosen_suffix[10]

        if self.rarity == "legendary":
            self.power = self.power*POWER_BASE**3
        elif self.rarity == "epic":
            self.power = self.power*POWER_BASE**2
        elif self.rarity == "rare":
            self.power = self.power*POWER_BASE
        elif self.rarity == "normal":
            pass
        self.power = self.power*self.base

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

    def getStats(self):
        return 'Attack: %d\nDefense: %d\nHealth: %d\nSpeed: %d\nMagic: %d'\
     % (self.attack, self.defense, self.health, self.speed, self.magic)

if __name__ == "__main__":
    i = Item(100, 3)
    print(i.name)
    print(i.getStats())
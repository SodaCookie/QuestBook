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
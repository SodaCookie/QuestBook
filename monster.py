import random
from moves import *
from constants import *

class Monster:

    def __init__(self, difficulty = 1, monster = "", power=0): # ELITE AND BOSS MONSTER HAVE GUARENTEED ABILITES, ABILTY IS BASED ON MAGIC
        self.difficulty = difficulty
        self.effects = []
        self.args = []
        self.moves = [MonsterDamage("monster-damage", self)]
        self.default_move = Move("do-nothing")
        self.next_move = self.default_move
        self.name = ""
        self.monster = monster
        self.monstertype = ""
        self.attack = 0
        self.defense = 0
        self.magic = 0
        self.current_health = 100
        self.health = 100
        self.speed = 10
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

    def deal_damage(self, battle, damage, damage_type):
        for effect in self.effects:
            damage = effect.on_damage(battle, damage, damage_type)
        damage = damage - self.defense
        if damage <= 0:
            damage = 1
        self.current_health -= damage
        return damage

    def handle(self, battle):
        log = ""

        # Determining what move to do (AI Portion)
        self.next_move = random.choice(self.moves)

        log += self.next_move.cast(battle, *self.args)

        # Remove the effect after the duration is gone
        for effect in self.effects[:]:
            effect.duration -= 1
            if effect.duration <= 0:
                self.effects.remove(effect)
        self.next_move = self.default_move
        self.args = []
        return log

    def set_args(*args):
        self.args = args

    def add_effect(self, effect):
        self.effects.append(effect)

    def toString(self):
        return 'Name: %s\nAttack: %d\nDefense: %d\nHealth: %d\nSpeed: %d'\
     % (self.name, self.attack, self.defense, self.health, self.speed)
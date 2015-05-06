from item import *
from constants import *
from builtin_moves import *
import math

class Player:

    def __init__(self, name):
        self.name = name
        self.effects = []
        self.moves = []
        self.add_move(magic_skills[0])
        self.add_move(magic_skills[1])
        self.add_move(magic_skills[2])
        self.fallen = False
        self.drop = None # tmp variable for dropped items
        self.args = []
        self.default_move = self.moves[0]
        self.next_move = self.default_move
        self.attack = 5
        self.defense = 0
        self.magic = 5
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

    def config_for_new_battle(self):
        self.current_health = self.health
        self.drop = None
        self.effects = []
        self.update()

    def equip(self, item):
        """Try to equip item into the slot"""
        self.equipment[item.slot] = item
        self.update()

    def handle(self, battle):
        self.next_move.cast(battle, *self.args)
        log = self.next_move.get_message()

        # Remove the effect after the duration is gone
        for effect in self.effects[:]:
            effect.duration -= 1
            if effect.duration <= 0:
                self.effects.remove(effect)
        self.next_move = self.default_move
        self.args = []
        return log

    def deal_damage(self, battle, damage, damage_type):
        for effect in self.effects:
            damage = effect.on_damage(battle, damage, damage_type)
        damage = round(damage - self.get_defense())
        if damage <= 0:
            damage = 1
        self.current_health -= damage
        return damage

    def get_attack(self):
        attack = self.attack
        for effect in self.effects:
            attack = effect.on_get_stat(attack, "attack")
        return int(attack)

    def get_defense(self):
        defense = self.defense
        for effect in self.effects:
            defense = effect.on_get_stat(defense, "defense")
        return int(defense)

    def get_speed(self):
        speed = self.speed
        for effect in self.effects:
            speed = effect.on_get_stat(speed, "speed")
        return int(speed)

    def get_magic(self):
        magic = self.magic
        for effect in self.effects:
            magic = effect.on_get_stat(magic, "magic")
        return int(magic)

    def get_level(self):
        return int(LEVEL_CONSTANT*math.sqrt(self.experience))+1

    def is_level_up(self):
        if self.get_level() > self.level:
            return True
        return False

    def level_up(self):
        for i in range(self.get_level() - self.level):
            for item in self.equipment.values():
                attack += item.attack
                defense += item.defense
                health += item.health
                speed += item.speed
                magic += item.magic
            total = attack + defense + health + speed + magic
            attack_weight = attack/total
            defense_weight = defense/total
            health_weight = health/total
            speed_weight = speed/total
            magic_weight = magic/total
            self.attack += attack_weight * POINTS_PER_LEVEL
            self.defense += defense_weight * POINTS_PER_LEVEL
            self.health += health_weight * POINTS_PER_LEVEL
            self.speed += speed_weight * POINTS_PER_LEVEL
            self.magic += magic_weight * POINTS_PER_LEVEL
        self.level = self.get_level();

    def set_args(*args):
        self.args = args

    def add_effect(self, effect):
        self.effects.append(effect)

    def add_move(self, move):
        self.moves.append(move)
        move.set_caster(self)

    def save(self):
        pass

    def load(self, file):
        pass

    def getStats(self):
        return ' | EXP: %d | LVL %d\n========================\nAttack: %d\nDefense: %d\nHealth: %d\\%d\nSpeed: %d\nMagic: %d'\
     % (self.experience, self.get_level(), self.attack, self.defense, self.current_health, self.health, self.speed, self.magic)
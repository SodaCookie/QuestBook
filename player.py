from item import *
from moves import *

class Player:

    def __init__(self, name):
        self.name = name
        self.effects = []
        self.moves = [Damage("attack", self), DefyDeath("defy-death", self)]
        self.args = []
        self.default_move = self.moves[0]
        self.next_move = self.default_move
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

    def handle(self, battle):
        log = ""
        log += self.next_move.cast(battle, *self.args)

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
        damage = damage - self.defense
        if damage <= 0:
            damage = 1
        self.current_health -= damage
        return damage

    def set_args(*args):
        self.args = args

    def add_effect(self, effect):
        self.effects.append(effect)

    def getStats(self):
        return ' | EXP: %d | LVL %d\n========================\nAttack: %d\nDefense: %d\nHealth: %d\\%d\nSpeed: %d\nMagic: %d'\
     % (self.experience, self.level, self.attack, self.defense, self.current_health, self.health, self.speed, self.magic)
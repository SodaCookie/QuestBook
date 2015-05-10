class Effect:

    def __init__(self, name, duration):
        """'name' is the identifier used to identify the effect
        duration is used to indicate how long the effect will last on the target.
        Durations for each effect on a target are decreased by 1 after that
         character's turn"""
        self.name = name
        self.duration = duration
        self.active = True

    def remove(self):
        """When called any subsequent calls to this effect will be ignored as well as removed
        useful for 1 time effects"""
        self.duration = 0
        self.active = False

    def on_get_stat(self, value, stat_type):
        """Any time a character is asked for a stat this function will be called
        and the type of stat will be used to determine how the stat will be
        affected. Returned is the stat of the player"""
        return value

    def on_start_turn(self, battle, character):
        """Return a tuple index 0 true if you can go, return false if you can't (ie stun, dead), index 1 is the message"""
        return (True, "")

    def on_damage(self, battle, source, damage, damage_type):
        return damage

    def on_heal(self, battle, source, heal):
        return heal

    def on_cast(self, battle, source, move):
        pass

    def on_death(self, battle, character):
        """If truly dead then return True"""
        return True

    def on_end_turn(self, battle, character):
        """That is the end of the characters turn (not the WHOLE turn), returns message"""
        return ""

    def __str__(self):
        return "%s - Turn(s)%d" % (self.name.replace("-", " ").title(), self.duration)


class Block(Effect):

    def __init__(self, duration, percentage, damage_type, name):
        super().__init__(name, duration)
        self.percentage = percentage
        self.damage_type = damage_type

    def on_damage(self, battle, source, damage, damage_type):
        if damage_type == self.damage_type:
            return damage*self.percentage
        return damage


class BlockAllSingle(Effect):

    def __init__(self, duration, percentage, name):
        super().__init__(name, duration)
        self.percentage = percentage

    def on_damage(self, battle, source, damage, damage_type):
        if damage_type == "true":
            return damage
        self.remove()
        return damage*self.percentage


class Slow(Effect):

    def __init__(self, duration, mod):
        super().__init__("slowed", duration)
        self.mod = mod

    def on_get_stat(self, value, stat_type):
        if stat_type == "speed":
            return value*self.mod
        return value


class Burn(Effect):

    def __init__(self, duration, caster, target, ratio):
        super().__init__("burning", duration)
        self.caster = caster
        self.damage = caster.get_magic() * ratio

    def on_end_turn(self, battle, character):
        damage = character.deal_damage(battle, self.caster, self.damage, "fire")
        return "\n" + character.name + " burned for " + str(damage) + " damage."


class Poison(Effect):

    def __init__(self, duration, caster, target, ratio):
        super().__init__("poisoned", duration)
        self.caster = caster
        self.damage = caster.get_magic() * ratio

    def on_end_turn(self, battle, character):
        damage = character.deal_damage(battle, self.caster, self.damage, "nature")
        return "\n" + character.name + " poisoned for " + str(damage) + " damage."


class Armor(Effect):

    def __init__(self, duration, mod):
        super().__init__("slowed", duration)
        self.mod = mod

    def on_get_stat(self, value, stat_type):
        if stat_type == "defense":
            return value*self.mod
        return value


class ReduceArmor(Effect):

    def __init__(self, duration, mod, name):
        super().__init__(name, duration)
        self.mod = mod

    def on_get_stat(self, value, stat_type):
        if stat_type == "defense":
            return value*self.mod
        return value


class ReduceAttack(Effect):

    def __init__(self, duration, mod, name):
        super().__init__(name, duration)
        self.mod = mod

    def on_get_stat(self, value, stat_type):
        if stat_type == "attack":
            return value*self.mod
        return value


class ReduceMagic(Effect):

    def __init__(self, duration, caster, target, mod, name):
        super().__init__(name, duration)
        self.amount = mod * caster.get_magic()

    def on_get_stat(self, value, stat_type):
        if stat_type == "magic":
            return value - self.amount if value - self.amount > 0 else 0
        return value


class IncreaseStat(Effect):

    def __init__(self, duration, mod, stat_type, name):
        super().__init__(name, duration)
        self.mod = mod

    def on_get_stat(self, value, stat_type):
        if stat_type == stat_type:
            return value * self.mod
        return value


class Combo(Effect):

    def __init__(self, duration, caster, target, spell, mod):
        super().__init__("melted", duration)
        self.caster = caster
        self.target = target
        self.spell = spell
        self.mod = mod
        self.counter = 1

    def on_damage(self, battle, source, damage, damage_type):
        if source == self.caster and self.spell == source.next_move.name:
            self.counter += 1
            return damage * self.mod ** self.counter
        elif source == self.caster:
            self.duration = 0
            return damage
        else:
            return damage


class Amplify(Effect):

    def __init__(self, duration, effect_type, mod, name):
        super().__init__(name, duration)
        self.mod = mod
        self.effect_type

    def on_damage(self, battle, source, damage, damage_type):
        if damage_type == self.effect_type:
            return damage * self.mod
        return damage


class BoostSingle(Effect):

    def __init__(self, duration, stype, mod, name):
        super().__init__(name, duration)
        self.mod = mod
        self.stype = stype

    def on_get_stat(self, value, stat_type):
        if self.stype == stat_type:
            return value*self.mod
        return value


class LowerAccuracy(Effect):

    def __init__(self, duration, amount, name):
        super().__init__(name, duration)
        self.amount = amount

    def on_cast(self, battle, source, move):
        move.set_accuracy(move.accuracy-self.amount)


class SolarBeam(Effect):
    def __init__(self, duration, caster, target):
        super().__init__("solar-beam", duration)
        self.target = target
        self.caster = caster

    def on_start_turn(self, battle, character):
        dam = self.target.deal_damage(battle, self.caster, self.caster.get_magic() * 2, "nature")
        return (False, self.caster.name + " dealt " + str(dam) + " nature damage to " + self.target.name + ".\n")

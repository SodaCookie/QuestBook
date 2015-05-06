class Effect:

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def on_get_stat(self, value, stat_type):
        """Any time a character is asked for a stat this function will be called
        and the type of stat will be used to determine how the stat will be
        affected. Returned is the stat of the player"""
        return value

    def on_start_turn(self, battle, character):
        """Return a tuple index 0 true if you can go, return false if you can't (ie stun, dead), index 1 is the message"""
        return (True, "")

    def on_damage(self, battle, damage, damage_type):
        return damage

    def on_heal(self, battle, heal):
        return heal

    def on_death(self, battle, character):
        """If truly dead then return True"""
        return True

    def on_end_turn(self, battle, character):
        """That is the end of the characters turn (not the WHOLE turn), returns message"""
        return ""


class Blocking(Effect):

    def __init__(self, duration, percentage, damage_type):
        super().__init__("blocking", duration)
        self.percentage = percentage
        self.damage_type = damage_type

    def on_damage(self, battle, damage, damage_type):
        if damage_type == self.damage_type:
            return damage*self.percentage
        return damage


class Slow(Effect):

    def __init__(self, duration, mod):
        super().__init__("slowed", duration)
        self.mod = mod

    def on_get_stat(self, value, stat_type):
        if stat_type == "speed":
            return value*self.mod
        return value

class Poison(Effect):

    def __init__(self, duration, damage):
        super().__init__("slowed", duration)
        self.damage = damage

    def on_end_turn(self, battle, character):
        damage = character.deal_damage(battle, self.damage, "poison")
        return character.name + " was dealt " + str(damage) + " poison damage.\n"


class Burn(Effect):

    def __init__(self, duration, caster, target, ratio):
        super().__init__("burning", duration)
        self.damage = caster.get_magic() * ratio

    def on_end_turn(self, battle, character):
        damage = character.deal_damage(battle, self.damage, "fire")
        return "\n" + character.name + " burned for " + str(damage) + " damage."

class Armor(Effect):

    def __init__(self, duration, mod):
        super().__init__("slowed", duration)
        self.mod = mod

    def on_get_stat(self, value, stat_type):
        if stat_type == "defense":
            return value*self.mod
        return value


class Fallen(Effect):

    def __init__(self, duration):
        super().__init__("fallen", duration)

    def on_start_turn(self, battle, character):
        return (False,"")
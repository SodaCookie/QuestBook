class Effect:

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def on_start_turn(self, battle, character):
        """Return true if you can go, return false if you can't (ie stun, dead)"""
        return True

    def on_damage(self, battle, damage, damage_type):
        return damage

    def on_heal(self, battle, heal):
        return heal

    def on_death(self, battle, character):
        """If truly dead then return True"""
        return True

    def on_end_turn(self, start, character):
        """That is the end of the characters turn (not the WHOLE turn)"""
        pass


class Blocking(Effect):

    def __init__(self, duration, percentage, damage_type):
        super().__init__("blocking", duration)
        self.percentage = percentage
        self.damage_type = damage_type

    def on_damage(self, battle, damage, damage_type):
        if damage_type == self.damage_type:
            return damage*self.percentage
        return damage

class Fallen(Effect):
    def __init__(self, duration):
        super().__init__("fallen", duration)

    def on_start_turn(self, battle, character):
        return False

class DefyDeath(Effect):

    def __init__(self, duration):
        super().__init__("defy-death", duration)

    def on_death(self, battle, character):
        character.current_health = character.health
        self.duration = 0
        return False
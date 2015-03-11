class Effect:

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def on_start_turn(self, battle, character):
        pass

    def on_damage(self, battle, damage):
        return damage

    def on_heal(self, battle, heal):
        return heal

    def on_death(self, battle, character):
        """If truly dead then return True"""
        return True

    def on_end_turn(self, start, character):
        pass

class Blocking(Effect):

    def __init__(self, duration, percentage):
        super().__init__("blocking", duration)
        self.percentage = percentage

    def on_damage(self, battle, damage):
        return damage*self.percentage
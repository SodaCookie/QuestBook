import random
import effects

class Move:

    def __init__(self, name, *args):
        self.name = name
        self.args = args

    def cast(self, *args):
        """Returns a string describing what happened. args are all arguments after the command.
        example: -heal player1 will have args = [player1]. Subclass effect. args[0] will always be the battle"""
        return ""


class Block(Move):

    def __init__(self, name, duration, caster):
        super().__init__(name)
        self.caster = caster
        self.duration = duration

    def cast(self, *args):
        self.caster.add_effect(effects.Blocking(self.duration, 0.5, "physical"))
        return self.caster + " has taken a defensive pose."


class Shield(Move):

    def __init__(self, name, duration, caster):
        super().__init__(name)
        self.caster = caster
        self.duration = duration

    def cast(self, *args):
        self.caster.add_effect(effects.Armor(self.duration, 1.5))
        return self.caster.name + " has cast shield on himself."


class Toxic(Move):

    def __init__(self, name, duration, caster, damage):
        super().__init__(name)
        self.caster = caster
        self.duration = duration
        self.damage = damage

    def cast(self, *args):
        target = None
        if len(args) < 2: # No argument was given
            target = args[0].monster
        else:
            if args[1] == "monster":
                target = args[0].monster
            else:
                for member in args[0].party:
                    if args[1] == member.name:
                        target = member
                        break
        if target:
            target.add_effect(effects.Poison(self.duration, self.damage))
            return target.name + " is poisoned."
        return "Couldn't find a target."


class Damage(Move):

    def __init__(self, name, caster):
        super().__init__(name)
        self.caster = caster

    def cast(self, *args):
        target = None
        if len(args) < 2: # No argument was given
            target = args[0].monster
        else:
            if args[1] == "monster":
                target = args[0].monster
            else:
                for member in args[0].party:
                    if args[1] == member.name:
                        target = member
                        break
        if target:
            damage_dealt = target.deal_damage(args[0], self.caster.get_attack(), "physical")
            return self.caster.name + " dealt " + str(damage_dealt) + " to " + target.name + "."
        return "Couldn't find a target."


class DamageSlow(Move):

    def __init__(self, name, duration, caster):
        super().__init__(name)
        self.caster = caster
        self.duration = duration

    def cast(self, *args):
        target = None
        if len(args) < 2: # No argument was given
            target = args[0].monster
        else:
            if args[1] == "monster":
                target = args[0].monster
            else:
                for member in args[0].party:
                    if args[1] == member.name:
                        target = member
                        break
        if target:
            damage_dealt = target.deal_damage(args[0], self.caster.get_attack()*0.5, "physical")
            target.add_effect(effects.Slow(self.duration, 0.5))
            return self.caster.name + " dealt " + str(damage_dealt) + " to " + target.name + ".\n" + target.name + " is slowed."
        return "Couldn't find a target."

class MonsterDamage(Move):

    def __init__(self, name, caster):
        super().__init__(name)
        self.caster = caster

    def cast(self, *args):
        target = random.choice(args[0].party)
        damage_dealt = target.deal_damage(args[0], self.caster.get_attack(), "physical")
        return self.caster.name + " dealt " + str(damage_dealt) + " to " + target.name + "."


class MagicDamage(Move):

    def __init__(self, name, caster):
        super().__init__(name)
        self.caster = caster

    def cast(self, *args):
        target = None
        if len(args) < 2: # No argument was given
            target = args[0].monster
        else:
            if args[1] == "monster":
                target = args[0].monster
            else:
                for member in args[0].party:
                    if args[1] == member.name:
                        target = member
                        break
        if target:
            damage_dealt = target.deal_damage(args[0], self.caster.get_attack() * 0.2 + self.caster.get_magic() * 0.8, "magic")
            return self.caster.name + " dealt " + str(damage_dealt) + " magic damage to " + target.name + "."
        return "Couldn't find a target."
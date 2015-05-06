import random
import effects

class Move:

    def __init__(self, name, *args):
        self.name = name
        self.args = args
        self.caster = None

    def set_caster(self, caster):
        self.caster = caster

    def cast(self, *args):
        """Returns a string describing what happened. args are all arguments after the command.
        example: -heal player1 will have args = [player1]. Subclass effect. args[0] will always be the battle"""
        return ""


class Block(Move):

    def __init__(self, name, duration):
        super().__init__(name)
        self.duration = duration

    def cast(self, *args):
        self.caster.add_effect(effects.Blocking(self.duration, 0.5, "physical"))
        return self.caster.name + " has taken a defensive pose."


class Effect(Move):

    def __init__(self, name, effect):
        super().__init__(name)
        self.effect = effect

    def cast(self, *args):
        target = self.get_target(*args)
        if target:
            target.add_effect(self.effect)
            return self.caster.name + " cast " + self.effect.name.title() + " on " + target.name + "."
        return "Couldn't find a target."

    def get_target(self, *args):
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
        return target

class Damage(Move):

    def __init__(self, name, effect, scale=1):
        super().__init__(name)
        self.effect = effect
        self.scale = scale

    def cast(self, *args):
        target = self.get_target(*args)
        if target:
            damage_dealt = target.deal_damage(args[0], self.scale*self.caster.get_attack(), "physical")
            return self.caster.name + " dealt " + str(damage_dealt) + " to " + target.name + "."
        return "Couldn't find a target."

    def get_target(self, *args):
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
        return target

class DamageEffect(Damage):

    def __init__(self, name, effect, scale=1):
        super().__init__(name, scale)
        self.effect = effect

    def cast(self, *args):
        target = self.get_target(*args)
        if target:
            damage_dealt = target.deal_damage(args[0], self.scale*self.caster.get_attack(), "physical")
            target.add_effect(self.effect)
            return self.caster.name + " dealt " + str(damage_dealt) + " to " + target.name + "."
        return "Couldn't find a target."


class MonsterDamage(Move):

    def cast(self, *args):
        target = random.choice(args[0].party)
        damage_dealt = target.deal_damage(args[0], self.caster.get_attack(), "physical")
        return self.caster.name + " dealt " + str(damage_dealt) + " to " + target.name + "."


class DamageMagic(Damage):

    def __init__(self, name, percentage=0.8, dtype="magic", scale=1):
        super().__init__(name, scale)
        self.percentage = percentage
        self.dtype = dtype

    def cast(self, *args):
        target = self.get_target(*args)
        if target:
            damage_dealt = target.deal_damage(args[0], self.scale*(self.caster.get_attack() * (1-self.percentage) + self.caster.get_magic() * self.percentage), self.dtype)
            return self.caster.name + " dealt " + str(damage_dealt) + " " + self.dtype + " damage to " + target.name + "."
        return "Couldn't find a target."

class DamageEffectMagic(Damage):

    def __init__(self, name, effect, percentage=0.8, dtype="magic", scale=1):
        super().__init__(name)
        self.percentage = percentage

    def cast(self, *args):
        target = self.get_target(*args)
        if target:
            damage_dealt = target.deal_damage(args[0], self.scale*(self.caster.get_attack() * (1-self.percentage) + self.caster.get_magic() * self.percentage), self.dtype)
            target.add_effect(self.effect)
            return self.caster.name + " dealt " + str(damage_dealt) + " " + self.dtype + " " +" damage to " + target.name + "."
        return "Couldn't find a target."

class DamageRecoilMagic(Damage):

    def __init__(self, name, recoil=0.1, percentage=0.8, dtype="magic", scale=1):
        super().__init__(name, scale)
        self.recoil = recoil
        self.percentage = percentage
        self.dtype = dtype

    def cast(self, *args):
        target = self.get_target(*args)
        if target:
            damage_dealt = target.deal_damage(args[0], self.scale*(self.caster.get_attack() * (1-self.percentage) + self.caster.get_magic() * self.percentage), self.dtype)
            print(self.scale*(self.caster.get_attack() * (1-self.percentage) + self.caster.get_magic() * self.percentage))
            self_damage_dealt = target.deal_damage(args[0], self.recoil*damage_dealt, self.dtype)
            return self.caster.name + " dealt " + str(damage_dealt) + " " + self.dtype + " " +" damage to " + target.name + ".\n" + self.caster.name + " took " + str(self_damage_dealt) + " in recoil."
        return "Couldn't find a target."
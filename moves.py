import random
import effects
import types

class Move:

    def __init__(self, name):
        if type(name) == str:
            self.name = name
            self.prev = None
        elif issubclass(type(name), Move):
            self.name = name.name
            self.prev = name
        self.caster = None
        self.msg = ""
        self.target = None

    def set_caster(self, caster):
        self.caster = caster
        if self.prev:
            self.prev.set_caster(caster)

    def get_target(self, *args):
        target = None
        if len(args) <= 1: # No argument was given
            target = args[0].monster
            return target
        else:
            if args[1] == "monster":
                target = args[0].monster
                return target
            else:
                for member in args[0].party:
                    if args[1] == member.name:
                        target = member
                        return target
        return target

    def message(self, msg):
        self.msg += msg

    def get_message(self):
        if self.prev:
            self.msg = self.prev.get_message() + "\n" + self.msg
        return self.msg

    def cast(self, *args):
        self.msg = ""
        self.target = self.get_target(*args)
        if self.prev:
            self.prev.cast(*args)
        self._cast(*args)

    def _cast(self, *args):
        """Override to create effects"""
        pass


class Effect(Move):

    def __init__(self, name, effect):
        super().__init__(name, move)
        self.effect = effect

    def _cast(self, *args):
        if self.target:
            self.target.add_effect(self.effect)
            self.message(self.caster.name + " cast " + self.effect.name.title() + " on " + self.target.name + ".")
        else:
            self.message("Couldn't find a target.")

class Damage(Move):

    def __init__(self, name, dtype="physical", scale=1):
        super().__init__(name)
        self.dtype = dtype
        self.scale = scale

    def _cast(self, *args):
        if self.target:
            damage_dealt = self.target.deal_damage(args[0], self.scale*self.caster.get_attack(), self.dtype)
            self.message(self.caster.name + " dealt " + str(damage_dealt) + " to " + self.target.name + ".")
        self.message("Couldn't find a target.")


class MagicDamage(Move):

    def __init__(self, name, dtype="magic", percentage=0.8, scale=1):
        super().__init__(name)
        self.dtype = dtype
        self.percentage = percentage
        self.scale = scale

    def _cast(self, *args):
        if self.target:
            damage_dealt = self.target.deal_damage(args[0], self.scale*(self.caster.get_attack() * (1-self.percentage) + self.caster.get_magic() * self.percentage), self.dtype)
            self.message(self.caster.name + " dealt " + str(damage_dealt) + " " + self.dtype + " damage to " + self.target.name + ".")
        else:
            self.message("Couldn't find a target.")


class Recoil(Move):

    def __init__(self, name, rdtype="physical", recoil=0.1):
        super().__init__(name)
        self.rdtype = rdtype # Return damage type
        self.recoil = recoil

    def _cast(self, *args):
        damage_dealt = self.caster.deal_damage(args[0], self.recoil*self.caster.get_attack(), self.rdtype)
        self.message(self.caster.name + " took " + str(damage_dealt) + " in recoil.")

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

class DamageEffectDynamicMagic(Damage):

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
            self_damage_dealt = target.deal_damage(args[0], self.recoil*damage_dealt, self.dtype)
            return self.caster.name + " dealt " + str(damage_dealt) + " " + self.dtype + " " +" damage to " + target.name + ".\n" + self.caster.name + " took " + str(self_damage_dealt) + " in recoil."
        return "Couldn't find a target."


if __name__ == "__main__":
    # Testing
    nmove = target_cast(damage(Move("test")))
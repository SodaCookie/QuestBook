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


class CastDynamicEffect(Move): # Dynamic effects get the castor's and target's stats past on to them

    def __init__(self, name, effect, duration, text="", *args):
        super().__init__(name)
        self.effect = effect
        self.text = text # To be displaced when sucessful cast
        self.duration = duration
        self.args = args

    def _cast(self, *args):
        if self.target:
            tmp_effect = self.effect(self.duration, self.caster, self.target, *self.args)
            self.target.add_effect(tmp_effect)
            self.message(self.text)
        else:
            self.message("Couldn't find a target.")


class CastEffect(Move):

    def __init__(self, name, effect, duration, text="", *args):
        super().__init__(name)
        self.effect = effect
        self.text = text # To be displaced when sucessful cast
        self.duration = duration
        self.args = args

    def _cast(self, *args):
        if self.target:
            tmp_effect = self.effect(self.duration, *self.args)
            self.target.add_effect(tmp_effect)
            self.message(self.text)
        else:
            self.message("Couldn't find a target.")


class Damage(Move):

    def __init__(self, name, dtype="physical", scale=1):
        super().__init__(name)
        self.dtype = dtype
        self.scale = scale

    def _cast(self, *args):
        if self.target:
            damage_dealt = self.target.deal_damage(args[0], self.caster, self.scale*self.caster.get_attack(), self.dtype)
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
            damage_dealt = self.target.deal_damage(args[0], self.caster, self.scale*(self.caster.get_attack() * (1-self.percentage) + self.caster.get_magic() * self.percentage), self.dtype)
            self.message(self.caster.name + " dealt " + str(damage_dealt) + " " + self.dtype + " damage to " + self.target.name + ".")
        else:
            self.message("Couldn't find a target.")


class Recoil(Move):

    def __init__(self, name, rdtype="physical", recoil=0.1):
        super().__init__(name)
        self.rdtype = rdtype # Return damage type
        self.recoil = recoil

    def _cast(self, *args):
        damage_dealt = self.caster.deal_damage(args[0], self.caster, self.recoil*self.caster.get_attack(), self.rdtype)
        self.message(self.caster.name + " took " + str(damage_dealt) + " in recoil.")


class MonsterDamage(Move):

    def _cast(self, *args):
        target = random.choice(args[0].party)
        damage_dealt = target.deal_damage(args[0], self.caster, self.caster.get_attack(), "physical")
        self.message(self.caster.name + " dealt " + str(damage_dealt) + " to " + target.name + ".")


if __name__ == "__main__":
    # Testing
    nmove = target_cast(damage(Move("test")))


class CastEffectSelf(CastEffect):
    def get_target(self, *args):
        return self.caster
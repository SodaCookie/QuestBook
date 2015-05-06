from moves import *
from effects import *

magic_skills = list()
magic_skills.append(MagicDamage("fireball", "fire", 1, 1.0))
magic_skills.append(MagicDamage("lava-burst", "fire", 1, 1.5))
magic_skills.append(Recoil(MagicDamage("solar-flare", "fire", 1, 3.0), "fire", 0.1))
magic_skills.append(CastDynamicEffect(MagicDamage("cinder-barrage", "fire", 1, 1.2), Burn, 3, "Target was burned.", 0.1))
magic_skills.append(CastEffect(MagicDamage("ice-blast", "frost", 0.8, 1.0), Slow, 2, "Target was slowed.", 0.5))
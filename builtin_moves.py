from moves import *

magic_skills = list()
magic_skills.append(DamageMagic("fireball", 1, "fire"))
magic_skills.append(DamageMagic("lava-burst", 1, "fire", 1.5))
magic_skills.append(DamageRecoilMagic("solar-flare", 0.1, 1, "fire", 3.0))
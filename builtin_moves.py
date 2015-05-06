from moves import *

magic_skills = list()
magic_skills.append(MagicDamage("fireball", "fire", 1, 1.0))
magic_skills.append(MagicDamage("lava-burst", "fire", 1, 1.5))
magic_skills.append(Recoil(MagicDamage("solar-flare", "fire", 1, 3.0), "fire", 0.1))
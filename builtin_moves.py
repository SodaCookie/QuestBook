from moves import *
from effects import *

skill_tree = dict()
skill_tree["attack"] = ["magic-blot", "heal", "smash", "mark"]
skill_tree["magic-bolt"] = ["fireball", "ice-blast", "thorn"]
skill_tree["fireball"] = ["lava-burst", "cinder-barrage"]
skill_tree["lava-burst"] = ["solar-flare", "flash-inferno"]
skill_tree["cinder-barrage"] = ["melting-strike", "hot-blaze"]
skill_tree["ice-blast"] = ["arctic-lance", "flash-freeze"]
skill_tree["arctic-lance"] = ["deep-freeze", "encase"]
skill_tree["flash-freeze"] = ["pierce", "blizzard"]
skill_tree["thorn"] = ["drain", "poison"]
skill_tree["drain"] = ["solar-beam", "leech"]
skill_tree["poison"] = []
skill_tree["smash"] = ["flurry"]
skill_tree["flurry"] = ["earth-strike", "solar-strike", "lunar-strike"]
skill_tree["earth-strike"] = ["barrier"]
skill_tree["solar-strike"] = ["enhance"]
skill_tree["lunar-strike"] = ["pacify"]
skill_tree["heal"] = []
skill_tree["greater-heal"] = ["multi-heal", "dot-heal"]
skill_tree["multi-heal"] = ["party-heal", "bounce-heal"]
skill_tree["dot-heal"] = ["heal-bonus", "percent-heal"]
skill_tree["mark"] = []

abilities = dict()
testing = Damage("ben-attack", "true", 100)
abilities["attack"] = Damage("attack")
abilities["block"] = CastEffectSelf("block", Block, 2, "[caster] has taken a defensive stance")
abilities["magic-bolt"] = MagicDamage("magic-bolt", "magic", 0.8, 1.0)
abilities["fireball"] = MagicDamage("fireball", "fire", 1, 1.0)
abilities["lava-burst"] = MagicDamage("lava-burst", "fire", 1, 1.5)
abilities["solar-flare"] = Recoil(MagicDamage("solar-flare", "fire", 1, 3.0), "fire", 0.1)
abilities["cinder-barrage"] = CastDynamicEffect(MagicDamage("cinder-barrage", "fire", 1, 1.2), Burn, 3, "[target] was burned.", 0.1)
abilities["melting-strike"] = CastEffect(MagicDamage("melting-strike", "fire", 1, 1.0), ReduceArmor, 3, "[target]'s defense was lowered by 20%", 0.8, "melted")
abilities["flash-inferno"] = CastDynamicEffect(MagicDamage("flash-inferno", "fire", 1, 0.6), Combo, 2, "", "flash-inferno", 1.5)
abilities["hot-blaze"] = CastEffect(MagicDamage("hot-blaze", "fire", 1, 1.0), Amplify, 4, "Fire resistance lowered by 40%.", "fire", 1.4, "decrease-fire-resistance")
abilities["ice-blast"] = CastEffect(MagicDamage("ice-blast", "frost", 0.8, 1.0), Slow, 2, "[target] was slowed.", 0.5)
abilities["arctic-lance"] = Compare("arctic-lance", lambda caster, target: True if caster.get_speed() > target.get_speed() else False, MagicDamage("arctic-lance", "frost", 0.8, 3.0), MagicDamage("arctic-lance", "frost", 0.8, 1.0))
abilities["flash-freeze"] = CastEffectSelf(MagicDamage("flash-freeze", "frost", 0.8, 1.0), Block, 3, "[caster] gained 20% fire resistance", 0.8, "fire", "chilled")
abilities["blizzard"] = Message(Repeat(MagicDamage("blizzard", "frost", 0.8, 0.4), 5), "[caster] unleashes a barrage of ice: ", True)
abilities["deep-freeze"] = CastEffect(MagicDamage("deep-freeze", "frost", 1, 1.0), IncreaseStat, 3, "[target] was in encased in ice", 1.3, "defense","Frost Armor")
abilities["encase"] = CastEffect(MagicDamage("encase", "frost", 1, 4.0), ReduceAttack, 3, "[target]'s attack was crippled.", 0.8, "Frost Armor")
abilities["pierce"] = MagicDamage("pierce", "true", 0.8, 0.8)
abilities["thorn"] = MagicDamage("thorn", "nature", 0.6, 1.2)
abilities["poison"] = CastDynamicEffect(MagicDamage("poison", "nature", 0.6, 0.5), Poison, 3, "[target] was poisoned.", 0.2)
abilities["heal"] = Heal("heal", 0.8, 1)

abilities["smash"] = Damage("smash", "physical", 1.2)
abilities["flurry"] = Message(Repeat(Damage("flurry", "physical", 0.4), 3), "[caster] attacks with a flurry of punches.", True)
abilities["earth-strike"] = ScaleDamage("earth-strike", "nature", "speed", 0.5, 1.2)
abilities["solar-strike"] = ScaleDamage("solar-strike", "fire", "speed", 0.5, 1.2)
abilities["lunar-strike"] = ScaleDamage("lunar-strike", "frost", "speed", 0.5, 1.2)
abilities["barrier"] = CastEffectSelf("barrier", BlockAllSingle, 2, "[caster] has taken a defensive stance", 0.2, "barrier")
abilities["enhance"] = CastEffect("enhance", BoostSingle, 2, "[caster] enhanced [target]'s next physical attack", "attack", 2, "enhance")
abilities["pacify"] = CastEffect("pacify", LowerAccuracy, 2, "[target] enters a calming state, lowering accuracy", 20, "pacified")
abilities["drain"] = HealSelf(MagicDamage("thorn", "nature", 0.6, 1.0), 0.2, 0.5)
abilities["leech"] = CastEffectSelf(CastDynamicEffect("leech", ReduceMagic, 2, "[caster] leeched magic from [target].", 0.2, "leeched"), IncreaseStat, 2, "", 1.2, "magic", "stolen-magic")
abilities["solar-beam"] = CastDynamicEffectSelf("solar-beam", SolarBeam, 2, "[caster] is charging solar-beam.")
abilities["heal"] = Heal("heal", 0.8, 1)
abilities["mark"] = CastEffect("mark", AmplifyAll, 2, "[target] is marked for death", 1.2, "marked")
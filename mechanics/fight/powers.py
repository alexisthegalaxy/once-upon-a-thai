import random
from math import log as ln

# from mechanics.fight.fighter import Fighter
#
#
# def deals_damage(al, fight, attacker: Fighter, receiver: Fighter, amount: float) -> float:
#     """
#     attacker and receiver can be Player or Opponent
#     """
#     damage_dealt = amount * attacker.attack / receiver.defense
#     receiver.hp -= damage_dealt
#     return damage_dealt
#
#
# def heals(al, fight, fighter: Fighter, amount):
#     health_healed = amount * fighter.healing_power
#     fighter.hp += health_healed
#
#
# def deals_vampiric_damage(al, fight, attacker, receiver, amount):
#     damage_dealt = deals_damage(al, fight, attacker, receiver, amount)
#     health_healed = damage_dealt / 2
#     attacker.hp += health_healed


def perform_attack(tones_effects, attacker, receiver):
    damage_amount = 1  # eventually, will be different for each word, rarer words being hard-hitters

    damage_multiplier = tones_effects.get("damage_multiplier", 1)
    damage_dealt = damage_amount * damage_multiplier * attacker.attack / receiver.defense

    time_multiplier = tones_effects.get("time_multiplier", 1)
    available_time = time_multiplier * receiver.time
    # The following formula returns 0.5 if available_time = 10, which is the default.
    probability_pass_test = min(max(0.5 * ln(available_time) / ln(10), 0.05), 0.95)
    if random.uniform(0, 1) > probability_pass_test:
        # then, test fails
        receiver.hp -= damage_dealt
        has_vampiric_effect = tones_effects.get("has_vampiric_effect", False)
        if has_vampiric_effect:
            attacker.hp += damage_dealt / 2


def apply_effects(tones_effects, attacker, receiver):
    if "reduce_time" in tones_effects:
        receiver.time *= tones_effects["reduce_time"]
    may_induce_flinching = tones_effects.get("may_induce_flinching", False)
    if may_induce_flinching:
        probability_flinches = min(max(0.5 * ln(receiver.flinching_resistance) / ln(10), 0.05), 0.95)
        receiver.flinched = random.uniform(0, 1) > probability_flinches


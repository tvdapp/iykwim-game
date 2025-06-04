from Abilities.SpecialAbility import SpecialAbility


class Teleportation(SpecialAbility):
    def use_special_ability(self):
        print("🌀 Teleportation activated! Instantly moving to any desired location!")
        return {"speed_bonus": 45, "mobility_multiplier": 3.0, "description": "Teleportation allows instant travel and unmatched battlefield mobility!"}
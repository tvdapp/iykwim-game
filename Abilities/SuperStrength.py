from Abilities.SpecialAbility import SpecialAbility


class SuperStrength(SpecialAbility):
    def use_special_ability(self):
        print("💪 Super Strength activated! Gained extra energy boost!")
        return {"energy_bonus": 20, "description": "Super Strength gives you extra energy!"}
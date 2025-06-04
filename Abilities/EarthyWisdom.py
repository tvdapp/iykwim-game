from Abilities.SpecialAbility import SpecialAbility


class EarthyWisdom(SpecialAbility):
    def use_special_ability(self):
        print("🌍 Roel (DJ Roomboter) activates Earthy Wisdom! Grounded solutions and practical insights!")
        return {"wisdom_bonus": 18, "resource_efficiency": 1.5, "description": "Earthy Wisdom provides practical solutions and efficient resource management!"}
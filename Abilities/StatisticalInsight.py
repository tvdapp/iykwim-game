from Abilities.SpecialAbility import SpecialAbility


class StatisticalInsight(SpecialAbility):
    def use_special_ability(self):
        print("📊 Mika (Barfika) activates Statistical Insight! Data patterns revealed!")
        return {"precision_bonus": 30, "critical_chance": 0.25, "description": "Statistical Insight provides predictive analysis and enhanced accuracy!"}

from Abilities.SpecialAbility import SpecialAbility


class BiologicalResilience(SpecialAbility):
    def use_special_ability(self):
        print("🧬 Phrits activates Biological Resilience! Enhanced recovery and disease resistance!")
        return {"health_bonus": 25, "recovery_rate": 2.0, "description": "Biological Resilience grants superior healing and immunity!"}
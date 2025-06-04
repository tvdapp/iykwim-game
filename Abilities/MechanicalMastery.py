from Abilities.SpecialAbility import SpecialAbility

class MechanicalMastery(SpecialAbility):
    def use_special_ability(self):
        print("🔧 Rick (Pringers) activates Mechanical Mastery! Precision bonus unlocked!")
        return {"precision_bonus": 15, "description": "Mechanical skills boost your precision!"}
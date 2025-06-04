from Abilities.SpecialAbility import SpecialAbility


class Invisibility(SpecialAbility):
    def use_special_ability(self):
        print("👻 Invisibility activated! Completely undetectable for a limited time!")
        return {"stealth_bonus": 50, "detection_immunity": True, "description": "Invisibility grants complete concealment from all forms of detection!"}
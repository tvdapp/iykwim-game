from Abilities.SpecialAbility import SpecialAbility


class MasterOfDisguise(SpecialAbility):
    def use_special_ability(self):
        print("🎭 Jordy (Snordy) activates Master of Disguise! Identity completely transformed!")
        return {"stealth_bonus": 40, "deception_skill": 28, "description": "Master of Disguise provides perfect camouflage and infiltration abilities!"}
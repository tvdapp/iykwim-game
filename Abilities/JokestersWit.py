from Abilities.SpecialAbility import SpecialAbility


class JokestersWit(SpecialAbility):
    def use_special_ability(self):
        print("😂 Casper activates Jokester's Wit! Confusing enemies with ghastly humor!")
        return {"confusion_bonus": 20, "morale_boost": 15, "description": "Jokester's Wit demoralizes enemies while boosting team spirit!"}
from Abilities.SpecialAbility import SpecialAbility


class ImaginativeCreativity(SpecialAbility):
    def use_special_ability(self):
        print("🎨 Alex activates Imaginative Creativity! Innovative solutions emerging!")
        return {"innovation_bonus": 22, "adaptability": 1.8, "description": "Imaginative Creativity unlocks unique approaches and flexible problem-solving!"}
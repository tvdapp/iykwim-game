from abc import ABC, abstractmethod

class SpecialAbility(ABC):
    @abstractmethod
    def use_special_ability(self):
        pass
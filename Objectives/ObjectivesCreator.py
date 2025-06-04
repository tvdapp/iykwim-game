from Objectives import ObjectivesList
from abc import ABC, abstractmethod

class ObjectivesCreator(ABC):
    @abstractmethod
    def generate_data(self) -> ObjectivesList:
        pass
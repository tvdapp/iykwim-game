from abc import ABC, abstractmethod

class ObjectivesCreator(ABC):
    @abstractmethod
    def generate_data(self):
        pass
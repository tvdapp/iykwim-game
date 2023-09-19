from abc import ABC, abstractmethod


class ColorStrategy(ABC):
    @abstractmethod
    def get_color(self):
        pass
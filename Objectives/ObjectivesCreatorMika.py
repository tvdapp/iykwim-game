from Objectives import ObjectivesCreator
from Objectives import ObjectivesList

class ObjectivesCreatorMika(ObjectivesCreator):
    def generate_data(self):
        return ObjectivesList(
            "Mika (Barfika)'s Objectives",
            [
                "Analyze Game Statistics",
                "Win a Sports Tournament",
                "Coach a Team",
                "Analyze Opponents",
                "Sports Record Breaker",
                "Trivia Master",
                "Collect Sports Memorabilia"
            ]
        )
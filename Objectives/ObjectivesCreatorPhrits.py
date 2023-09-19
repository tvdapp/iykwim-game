from Objectives import ObjectivesCreator
from Objectives import ObjectivesList

class ObjectivesCreatorPhrits(ObjectivesCreator):
    def generate_data(self) -> ObjectivesList:
        return ObjectivesList(
            "Phrits' Objectives",
            [
                "Collect Rare Plant Specimens",
                "Explore the Forest",
                "Analyze Microorganisms",
                "Complete Fitness Challenges",
                "Solve Biological Puzzles",
                "Help Other Friends"
            ]
        )

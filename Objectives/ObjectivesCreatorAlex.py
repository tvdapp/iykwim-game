from Objectives import ObjectivesCreator
from Objectives import ObjectivesList

# Define the Objectives class with objectives for Alex
class ObjectivesCreatorAlex(ObjectivesCreator):
    def generate_data(self):
        return ObjectivesList(
            "Alex's Smart and Creative Objectives",
            [
                "Create Whimsical Inventions with Technical Genius",
                "Craft Hilarious Stories and Entertain Friends",
                "Solve Technical Challenges with Innovation",
                "Host a Creative Workshop for Friends",
                "Explore the Limits of AI Knowledge",
                "Use Smart Strategies to Outwit Adversaries",
                "Share Technical Insights and Knowledge"
            ]
        )
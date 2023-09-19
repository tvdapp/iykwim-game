from Objectives import ObjectivesCreator
from Objectives import ObjectivesList

# Define the Objectives class with objectives for Rick
class ObjectivesCreatorRick(ObjectivesCreator):
    def generate_data(self):
        return ObjectivesList(
            "Rick (Pringers)'s Technical Objectives",
            [
                "Fix Broken Machinery with Precision",
                "Create Technical Marvels and Inventions",
                "Provide Technical Insights and Solutions",
                "Solve Complex Technical Challenges",
                "Host a Workshop on Mechanical Mastery",
                "Repair and Upgrade Friendships with Care",
                "Safely Handle Fireworks for New Year's"
            ]
        )
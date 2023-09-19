from Objectives import ObjectivesCreator
from Objectives import ObjectivesList

# Define the Objectives class with farming-related objectives for Roel
class ObjectivesCreatorRoel(ObjectivesCreator):
    def generate_data(self):
        return ObjectivesList(
            "Roel (DJ Roomboter)'s Farming Objectives",
            [
                "Tend to the Cows with Care",
                "Cultivate a Bountiful Harvest",
                "Share Farming Wisdom with Friends",
                "Solve Farm-Related Challenges",
                "Host a Barnyard Get-Together",
                "Explore Farming Adventures"
            ]
        )
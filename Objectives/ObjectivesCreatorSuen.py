from Objectives import ObjectivesCreator
from Objectives import ObjectivesList

# Define the Objectives class with objectives for Suen
class ObjectivesCreatorSuen(ObjectivesCreator):
    def generate_data(self):
        return ObjectivesList(
            "Suen (Suenpai)'s Gaming and Hacking Objectives",
            [
                "Master Virtual Realms and Conquer Games",
                "Optimize Strategies with Min-Max Techniques",
                "Solve Hacking Challenges with Expertise",
                "Achieve High Scores and Records in Games",
                "Host Game Nights and LAN Parties",
                "Outsmart Virtual and Real Adversaries",
                "Hack into the Digital Frontier"
            ]
        )
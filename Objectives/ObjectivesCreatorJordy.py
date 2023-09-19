from Objectives import ObjectivesCreator
from Objectives import ObjectivesList

# Define the Objectives class with additional objectives for Jordy
class ObjectivesCreatorJordy(ObjectivesCreator):
    def generate_data(self):
        return ObjectivesList(
            "Jordy (Snordy)'s Fun and Quirky Objectives",
            [
                "Solve Psychological Puzzles with a Twist",
                "Help Friends with Over-the-Top Relationship Challenges",
                "Master the Art of Disguise with Hilarious Outcomes",
                "Organize a Car Show with Funky Cars",
                "Navigate a Secret Date with Comical Mishaps",
                "Confuse Enemies with Wacky Disguises",
                "Solve Mysteries in Style, Complete with Dramatic Reveals"
            ]
        ).show_objectives()
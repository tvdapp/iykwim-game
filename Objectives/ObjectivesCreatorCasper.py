from Objectives import ObjectivesCreator
from Objectives import ObjectivesList

# Define the Objectives class with humorous objectives for Casper
class ObjectivesCreatorCasper(ObjectivesCreator):
    def generate_data(self):
        return ObjectivesList(
            "Casper's Objectives (Prepare for Punny Quests!)",
            [
                "Tell the Funniest Jokes in the Afterlife",
                "Confuse Enemies with Wordplay and Witticisms",
                "Help Friends with Language Puzzles, Ghostly or Otherwise",
                "Play Pun-tastic Pranks on Everyone",
                "Host a Jokester's Challenge",
                "Organize a Language Treasure Hunt",
                "Riddle Rendezvous: Create and Solve Clever Riddles",
                "Linguistic Shenanigans: Have Multilingual Conversations"
            ]
        )
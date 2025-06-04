
class QuestSystem:
    def __init__(self):
        self.friends = []
        self.objectives = []

    def add_friend(self, friend):
        self.friends.append(friend)

    def add_objective(self, friend, objective):
        if friend in self.friends:
            friend.add_objective(objective)
        else:
            print(f"Friend '{friend.name}' is not part of this quest system.")

    def complete_objective(self, friend, objective):
        if friend in self.friends:
            friend.complete_objective(objective)
        else:
            print(f"Friend '{friend.name}' is not part of this quest system.")

    def show_objectives(self, friend):
        if friend in self.friends:
            print(f"{friend.name}'s Objectives:")
            for objective in friend.show_objectives():
                print(f"- {objective}")
        else:
            print(f"Friend '{friend.name}' is not part of this quest system.")

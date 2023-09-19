

class Objective:

  def __init__(self, description):
    self.description = description

  def show_objective(self):
    print(f"- {self.description}")

  def get_objective(self):
    return self.description


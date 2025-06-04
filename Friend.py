import pygame

class Friend:
    def __init__(self, name, xy, special_ability, objective_creator, color_strategy, image_string, character_size):
        self.name = name
        self.health = 100
        self.special_ability = special_ability
        self.objectives_list = objective_creator.generate_data()
        self.color_strategy = color_strategy
        self.image = pygame.transform.scale(pygame.image.load(image_string), character_size)
        self.x = xy[0]
        self.y = xy[1]

    def use_special_ability(self):
        self.special_ability.use_special_ability()

    def take_damage(self, damage):
        self.health -= damage

    def is_alive(self):
        return self.health > 0

    def show_objectives(self):
        self.objectives_list.show_objectives()

    def get_random_objective(self):
        return self.objectives_list.get_random_objective()

    # def get_objectives(self):


    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_image(self): 
        return self.image
    
    def get_rect(self):
        rect = self.image.get_rect()

        rect.x = self.x
        rect.y = self.y

        return rect
    
    
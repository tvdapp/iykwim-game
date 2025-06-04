import pygame
import sys
import random
from Abilities.EarthyWisdom import EarthyWisdom
from Colors.BrownColor import BrownColor
from Colors.ElectricBlueColor import ElectricBlueColor

from Friend import Friend
from Abilities.MasterOfDisguise import MasterOfDisguise
from Abilities.JokestersWit import JokestersWit
from Colors.LightBlueColor import LightBlueColor
from Abilities.ImaginativeCreativity import ImaginativeCreativity
from Abilities.MechanicalMastery import MechanicalMastery
from Abilities.MinMaxMastery import MinMaxMastery
from Objectives.ObjectivesCreatorPhrits import ObjectivesCreatorPhrits
from Objectives.ObjectivesCreatorMika import ObjectivesCreatorMika
from Objectives.ObjectivesCreatorJordy import ObjectivesCreatorJordy

from Abilities.Invisibility import Invisibility
from Abilities.SuperStrength import SuperStrength
from Abilities.Teleportation import Teleportation
from Abilities.BiologicalResilience import BiologicalResilience
from Abilities.StatisticalInsight import StatisticalInsight

from Colors.GreenColor import GreenColor
from Colors.RedColor import RedColor
from Colors.BlueColor import BlueColor
from Colors.OrangeColor import OrangeColor
from Objectives.ObjectivesCreatorCasper import ObjectivesCreatorCasper
from Objectives.ObjectivesCreatorRoel import ObjectivesCreatorRoel
from Objectives.ObjectivesCreatorAlex import ObjectivesCreatorAlex
from Colors.PurpleColor import PurpleColor
from Objectives.ObjectivesCreatorRick import ObjectivesCreatorRick
from Colors.SteelGrayColor import SteelGrayColor
from Objectives.ObjectivesCreatorSuen import ObjectivesCreatorSuen

pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
FPS = 30
base_url = "resources/cutout"

character_size = (64, 128)

# Colors
WHITE = (255, 255, 255)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Friend Adventure Game")


def random_position():
    return random.randint(0, WIDTH - character_size[0]), random.randint(0, HEIGHT - character_size[1])

# Define objectives for your friends
# Create instances of your friends with objectives
phrits = Friend("Phrits", random_position(), BiologicalResilience(), ObjectivesCreatorPhrits(), GreenColor(), base_url + "/" + "phrits.png", character_size)
mika = Friend("Mika (Barfika)", random_position(), StatisticalInsight(), ObjectivesCreatorMika(), OrangeColor(), base_url + "/" + "mika.png", character_size)
jordy = Friend("Jordy (Snordy)", random_position(), MasterOfDisguise(), ObjectivesCreatorJordy(), RedColor(), base_url + "/" + "gurdy.png", character_size)
casper = Friend("Casper", random_position(), JokestersWit(), ObjectivesCreatorCasper(), LightBlueColor(), base_url + "/" + "casper.png", character_size)
roel = Friend("Roel (DJ Roomboter)", random_position(), EarthyWisdom(), ObjectivesCreatorRoel(), BrownColor(), base_url + "/" + "roel.png", character_size)
alex = Friend("Alex", random_position(), ImaginativeCreativity(), ObjectivesCreatorAlex(), PurpleColor(), base_url + "/" + "alex.png", character_size)
rick = Friend("Rick (Pringers)", random_position(), MechanicalMastery(), ObjectivesCreatorRick(), SteelGrayColor(), base_url + "/" + "pringers.png", character_size)
suen = Friend("Suen (Suenpai)", random_position(), MinMaxMastery(), ObjectivesCreatorSuen(), ElectricBlueColor(), base_url + "/" + "suenpai.png", character_size)

# Add more friends with objectives as needed

# List to store friend characters
friends = [phrits, mika, jordy, casper, roel, alex, rick, suen]  # Add your friends here



# Initial position for the player
your_character = pygame.Rect(0, 0, character_size[0], character_size[1])
your_character_image = pygame.transform.scale(pygame.image.load(base_url + "/" + "thijs.png"), character_size)

your_character.x, your_character.y = WIDTH // 2, HEIGHT // 2
player_speed = 5

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        your_character.x -= player_speed
    if keys[pygame.K_RIGHT]:
        your_character.x += player_speed
    if keys[pygame.K_UP]:
        your_character.y -= player_speed
    if keys[pygame.K_DOWN]:
        your_character.y += player_speed


    # Check for interactions with friends
    for friend in friends:
        if (
            your_character.x < friend.x + 50
            and your_character.x + 50 > friend.x
            and your_character.y < friend.y + 50
            and your_character.y + 50 > friend.y
        ):
            # The player is close to the friend, you can define interactions here
            print(f"Interacting with {friend.name}")
            # if friend.objectives_list:
            print(f"Hey! I'd like to {friend.get_random_objective().get_objective()}, could you maybe help me with that?")
                # print(f"{friend.name}'s Objectives:")
                # for objective in friend.show_objectives():
                    # print(f"- {objective}")


    # Update game logic here

    # Draw game objects here

    
    # For simplicity, we'll draw each friend as a colored rectangle
    # w, h = character_size
    # player.x = max(0, min(friend.x, WIDTH - w))
    # player.y = max(0, min(friend.y, HEIGHT - h))
    
    # # Draw the player character (a simple rectangle for now)

    # pygame.draw.rect(screen, (0, 0, 255), (player.x, player.y, 50, 50))
    # Keep your character within the screen boundaries
    your_character.x = max(0, min(your_character.x, WIDTH - your_character.width))
    your_character.y = max(0, min(your_character.y, HEIGHT - your_character.height))


    # Clear the screen
    screen.fill(WHITE)

    # Draw friend characters
    for friend in friends:
        screen.blit(friend.get_image(), friend.get_rect().topleft)
        # pygame.draw.rect(screen, friend.color_strategy.get_color(), (friend.x, friend.y, 50, 50))


    # Draw the player character (a simple rectangle for now)
    screen.blit(your_character_image, your_character.topleft)


    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()

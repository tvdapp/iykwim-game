import pygame
import sys
import random
import math
from enum import Enum

# Import all the required modules
from Friend import Friend

# Import abilities
from Abilities.BiologicalResilience import BiologicalResilience
from Abilities.StatisticalInsight import StatisticalInsight
from Abilities.MasterOfDisguise import MasterOfDisguise
from Abilities.JokestersWit import JokestersWit
from Abilities.EarthyWisdom import EarthyWisdom
from Abilities.ImaginativeCreativity import ImaginativeCreativity
from Abilities.MechanicalMastery import MechanicalMastery
from Abilities.MinMaxMastery import MinMaxMastery

# Import colors
from Colors.GreenColor import GreenColor
from Colors.OrangeColor import OrangeColor
from Colors.RedColor import RedColor
from Colors.LightBlueColor import LightBlueColor
from Colors.BrownColor import BrownColor
from Colors.PurpleColor import PurpleColor
from Colors.SteelGrayColor import SteelGrayColor
from Colors.ElectricBlueColor import ElectricBlueColor

# Import objective creators
from Objectives.ObjectivesCreatorPhrits import ObjectivesCreatorPhrits
from Objectives.ObjectivesCreatorMika import ObjectivesCreatorMika
from Objectives.ObjectivesCreatorJordy import ObjectivesCreatorJordy
from Objectives.ObjectivesCreatorCasper import ObjectivesCreatorCasper
from Objectives.ObjectivesCreatorRoel import ObjectivesCreatorRoel
from Objectives.ObjectivesCreatorAlex import ObjectivesCreatorAlex
from Objectives.ObjectivesCreatorRick import ObjectivesCreatorRick
from Objectives.ObjectivesCreatorSuen import ObjectivesCreatorSuen

class GameState(Enum):
    MAIN_MENU = 1
    PLAYING = 2
    QUEST_DIALOG = 3
    MINI_GAME = 4
    GAME_OVER = 5
    VICTORY = 6

class QuestGame:
    def __init__(self):
        pygame.init()
        
        # Constants
        self.WIDTH, self.HEIGHT = 1200, 800
        self.FPS = 60
        self.character_size = (64, 128)
        self.base_url = "resources/cutout"
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (128, 128, 128)
        self.LIGHT_GRAY = (200, 200, 200)
        
        # Initialize screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("IYKWIM: Friend Quest Adventure")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.state = GameState.MAIN_MENU
        self.running = True
        
        # Player stats
        self.player_energy = 100
        self.max_energy = 100
        self.score = 0
        self.completed_quests = 0
        self.friendship_points = 0
        
        # Game objects
        self.friends = []
        self.current_friend = None
        self.current_quest = None
        self.active_quests = []
        self.completed_friends = set()
        
        # Mini-game variables
        self.mini_game_type = None
        self.mini_game_progress = 0
        self.mini_game_target = 100
        self.mini_game_time = 0
        self.mini_game_duration = 5.0  # seconds
        
        # Initialize game objects
        self.setup_game()
        
    def setup_game(self):
        """Initialize friends and player"""
        # Create friends with their unique properties
        friends_data = [
            ("Phrits", BiologicalResilience(), ObjectivesCreatorPhrits(), GreenColor(), "phrits.png"),
            ("Mika", StatisticalInsight(), ObjectivesCreatorMika(), OrangeColor(), "mika.png"),
            ("Jordy", MasterOfDisguise(), ObjectivesCreatorJordy(), RedColor(), "gurdy.png"),
            ("Casper", JokestersWit(), ObjectivesCreatorCasper(), LightBlueColor(), "casper.png"),
            ("Roel", EarthyWisdom(), ObjectivesCreatorRoel(), BrownColor(), "roel.png"),
            ("Alex", ImaginativeCreativity(), ObjectivesCreatorAlex(), PurpleColor(), "alex.png"),
            ("Rick", MechanicalMastery(), ObjectivesCreatorRick(), SteelGrayColor(), "pringers.png"),
            ("Suen", MinMaxMastery(), ObjectivesCreatorSuen(), ElectricBlueColor(), "suenpai.png"),
        ]
        
        for name, ability, objective_creator, color, image in friends_data:
            position = self.random_position()
            friend = Friend(name, position, ability, objective_creator, color, 
                          f"{self.base_url}/{image}", self.character_size)
            friend.happiness = 50  # Add happiness system
            friend.quest_completed = False
            self.friends.append(friend)
        
        # Create player
        self.player = pygame.Rect(self.WIDTH // 2, self.HEIGHT // 2, 
                                self.character_size[0], self.character_size[1])
        try:
            self.player_image = pygame.transform.scale(
                pygame.image.load(f"{self.base_url}/thijs.png"), self.character_size)
        except:
            # Fallback if image doesn't exist
            self.player_image = pygame.Surface(self.character_size)
            self.player_image.fill(self.BLUE)
        
        self.player_speed = 5
        
    def random_position(self):
        """Generate random position that doesn't overlap with player start"""
        while True:
            x = random.randint(50, self.WIDTH - self.character_size[0] - 50)
            y = random.randint(50, self.HEIGHT - self.character_size[1] - 50)
            # Make sure it's not too close to player start position
            if abs(x - self.WIDTH // 2) > 100 or abs(y - self.HEIGHT // 2) > 100:
                return (x, y)
    
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.state == GameState.MAIN_MENU:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.PLAYING
                elif self.state == GameState.QUEST_DIALOG:
                    if event.key == pygame.K_y:
                        self.accept_quest()
                    elif event.key == pygame.K_n:
                        self.decline_quest()
                elif self.state == GameState.MINI_GAME:
                    if event.key == pygame.K_SPACE:
                        self.mini_game_progress += 10
                elif self.state in [GameState.GAME_OVER, GameState.VICTORY]:
                    if event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_q:
                        self.running = False
    
    def update(self):
        """Update game logic based on current state"""
        if self.state == GameState.PLAYING:
            self.update_playing()
        elif self.state == GameState.MINI_GAME:
            self.update_mini_game()
    
    def update_playing(self):
        """Update main gameplay"""
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.x -= self.player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.x += self.player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.y -= self.player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.y += self.player_speed
        
        # Keep player within bounds
        self.player.x = max(0, min(self.player.x, self.WIDTH - self.player.width))
        self.player.y = max(0, min(self.player.y, self.HEIGHT - self.player.height))
        
        # Check for friend interactions
        for friend in self.friends:
            if not friend.quest_completed and self.check_collision(self.player, friend.get_rect()):
                self.current_friend = friend
                self.current_quest = friend.get_random_objective()
                self.state = GameState.QUEST_DIALOG
                break
        
        # Regenerate energy slowly
        if self.player_energy < self.max_energy:
            self.player_energy += 0.1
            self.player_energy = min(self.player_energy, self.max_energy)
        
        # Check win condition
        if len(self.completed_friends) >= len(self.friends):
            self.state = GameState.VICTORY
    
    def check_collision(self, rect1, rect2):
        """Check if two rectangles collide"""
        return rect1.colliderect(rect2)
    
    def accept_quest(self):
        """Accept the current quest and start mini-game"""
        if self.player_energy >= 20:  # Cost energy to help friends
            self.player_energy -= 20
            self.state = GameState.MINI_GAME
            self.setup_mini_game()
        else:
            # Not enough energy, go back to playing
            self.state = GameState.PLAYING
            self.current_friend = None
            self.current_quest = None
    
    def decline_quest(self):
        """Decline the current quest"""
        self.state = GameState.PLAYING
        self.current_friend = None
        self.current_quest = None
    
    def setup_mini_game(self):
        """Set up the mini-game based on the friend's ability"""
        ability_name = type(self.current_friend.special_ability).__name__
        
        # Different mini-games based on abilities
        mini_games = {
            'SuperStrength': 'button_mash',
            'MechanicalMastery': 'precision',
            'StatisticalInsight': 'pattern',
            'ImaginativeCreativity': 'rhythm',
            'JokestersWit': 'timing',
            'BiologicalResilience': 'endurance',
            'MasterOfDisguise': 'stealth',
            'MinMaxMastery': 'strategy'
        }
        
        self.mini_game_type = mini_games.get(ability_name, 'button_mash')
        self.mini_game_progress = 0
        self.mini_game_target = 100
        self.mini_game_time = 0
        self.mini_game_duration = 5.0
    
    def update_mini_game(self):
        """Update mini-game logic"""
        self.mini_game_time += 1/self.FPS
        
        # Different mechanics for different mini-games
        if self.mini_game_type == 'endurance':
            # Automatic progress that player must maintain
            self.mini_game_progress += 0.5
            # Add some decay
            if random.random() < 0.1:
                self.mini_game_progress -= 2
        elif self.mini_game_type == 'precision':
            # Slower progress, needs precise timing
            pass  # Only space bar adds progress
        elif self.mini_game_type == 'rhythm':
            # Add automatic rhythm bonus
            if int(self.mini_game_time * 2) % 2 == 0:
                self.mini_game_progress += 0.2
        
        # Check mini-game completion
        if self.mini_game_time >= self.mini_game_duration:
            self.complete_mini_game()
        elif self.mini_game_progress >= self.mini_game_target:
            self.complete_mini_game()
        elif self.mini_game_progress < 0:
            self.fail_mini_game()
    
    def complete_mini_game(self):
        """Complete the mini-game successfully"""
        success = self.mini_game_progress >= self.mini_game_target * 0.7  # 70% success threshold
        
        if success:
            # Reward player
            self.score += 100
            self.completed_quests += 1
            self.friendship_points += 10
            self.current_friend.happiness += 20
            self.current_friend.quest_completed = True
            self.completed_friends.add(self.current_friend.name)
            
            # Use friend's special ability as bonus
            self.current_friend.use_special_ability()
            
        else:
            # Partial reward for trying
            self.score += 25
            self.current_friend.happiness += 5
        
        # Return to main game
        self.state = GameState.PLAYING
        self.current_friend = None
        self.current_quest = None
        
        # Check if energy is too low
        if self.player_energy <= 0:
            self.state = GameState.GAME_OVER
    
    def fail_mini_game(self):
        """Fail the mini-game"""
        self.player_energy -= 10
        self.current_friend.happiness -= 5
        self.state = GameState.PLAYING
        self.current_friend = None
        self.current_quest = None
    
    def restart_game(self):
        """Restart the game"""
        self.__init__()
    
    def draw(self):
        """Draw everything based on current state"""
        self.screen.fill(self.WHITE)
        
        if self.state == GameState.MAIN_MENU:
            self.draw_main_menu()
        elif self.state == GameState.PLAYING:
            self.draw_playing()
        elif self.state == GameState.QUEST_DIALOG:
            self.draw_quest_dialog()
        elif self.state == GameState.MINI_GAME:
            self.draw_mini_game()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        elif self.state == GameState.VICTORY:
            self.draw_victory()
        
        pygame.display.flip()
    
    def draw_main_menu(self):
        """Draw the main menu"""
        title = self.font.render("IYKWIM: Friend Quest Adventure", True, self.BLACK)
        subtitle = self.small_font.render("Help your friends complete their objectives!", True, self.GRAY)
        instruction = self.small_font.render("Press SPACE to start", True, self.BLACK)
        
        title_rect = title.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 - 50))
        subtitle_rect = subtitle.get_rect(center=(self.WIDTH//2, self.HEIGHT//2))
        instruction_rect = instruction.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 + 50))
        
        self.screen.blit(title, title_rect)
        self.screen.blit(subtitle, subtitle_rect)
        self.screen.blit(instruction, instruction_rect)
    
    def draw_playing(self):
        """Draw the main game"""
        # Draw friends
        for friend in self.friends:
            # Draw glow effect for incomplete quests
            if not friend.quest_completed:
                glow_color = (*friend.color_strategy.get_color(), 100)
                glow_surf = pygame.Surface((80, 80), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, glow_color, (40, 40), 40)
                self.screen.blit(glow_surf, (friend.x - 8, friend.y - 8))
            
            # Draw friend
            self.screen.blit(friend.get_image(), friend.get_rect().topleft)
            
            # Draw happiness bar
            bar_width = 50
            bar_height = 8
            bar_x = friend.x + (self.character_size[0] - bar_width) // 2
            bar_y = friend.y - 15
            
            pygame.draw.rect(self.screen, self.RED, (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(self.screen, self.GREEN, (bar_x, bar_y, 
                           int(bar_width * friend.happiness / 100), bar_height))
        
        # Draw player
        self.screen.blit(self.player_image, self.player.topleft)
        
        # Draw UI
        self.draw_ui()
    
    def draw_quest_dialog(self):
        """Draw the quest dialog"""
        # Draw background (playing screen with overlay)
        self.draw_playing()
        
        # Draw dialog box
        dialog_width = 600
        dialog_height = 200
        dialog_x = (self.WIDTH - dialog_width) // 2
        dialog_y = (self.HEIGHT - dialog_height) // 2
        
        pygame.draw.rect(self.screen, self.WHITE, (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(self.screen, self.BLACK, (dialog_x, dialog_y, dialog_width, dialog_height), 3)
        
        # Draw text
        if self.current_friend and self.current_quest:
            friend_text = self.font.render(f"{self.current_friend.name} says:", True, self.BLACK)
            quest_text = self.small_font.render(f"'{self.current_quest.get_objective()}'", True, self.BLACK)
            energy_text = self.small_font.render(f"Cost: 20 Energy (You have: {int(self.player_energy)})", True, self.RED)
            choice_text = self.small_font.render("Help them? (Y/N)", True, self.BLACK)
            
            y_offset = dialog_y + 20
            self.screen.blit(friend_text, (dialog_x + 20, y_offset))
            y_offset += 40
            self.screen.blit(quest_text, (dialog_x + 20, y_offset))
            y_offset += 30
            self.screen.blit(energy_text, (dialog_x + 20, y_offset))
            y_offset += 30
            self.screen.blit(choice_text, (dialog_x + 20, y_offset))
    
    def draw_mini_game(self):
        """Draw the mini-game"""
        # Background
        self.screen.fill(self.LIGHT_GRAY)
        
        # Title
        title = self.font.render(f"Helping {self.current_friend.name}!", True, self.BLACK)
        title_rect = title.get_rect(center=(self.WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Progress bar
        bar_width = 400
        bar_height = 40
        bar_x = (self.WIDTH - bar_width) // 2
        bar_y = 300
        
        pygame.draw.rect(self.screen, self.RED, (bar_x, bar_y, bar_width, bar_height))
        progress_width = int(bar_width * (self.mini_game_progress / self.mini_game_target))
        pygame.draw.rect(self.screen, self.GREEN, (bar_x, bar_y, progress_width, bar_height))
        pygame.draw.rect(self.screen, self.BLACK, (bar_x, bar_y, bar_width, bar_height), 3)
        
        # Instructions
        instructions = {
            'button_mash': "Press SPACE rapidly!",
            'precision': "Press SPACE at the right moment!",
            'endurance': "Maintain progress! Press SPACE when it drops!",
            'rhythm': "Press SPACE to the rhythm!",
            'timing': "Wait for the perfect moment!",
            'pattern': "Follow the pattern! Press SPACE!",
            'stealth': "Press SPACE quietly and carefully!",
            'strategy': "Think strategically! Press SPACE wisely!"
        }
        
        instruction = self.small_font.render(instructions.get(self.mini_game_type, "Press SPACE!"), True, self.BLACK)
        instruction_rect = instruction.get_rect(center=(self.WIDTH//2, 400))
        self.screen.blit(instruction, instruction_rect)
        
        # Timer
        time_left = max(0, self.mini_game_duration - self.mini_game_time)
        timer_text = self.small_font.render(f"Time: {time_left:.1f}s", True, self.BLACK)
        self.screen.blit(timer_text, (50, 50))
        
        # Progress text
        progress_text = self.small_font.render(f"Progress: {int(self.mini_game_progress)}/{self.mini_game_target}", True, self.BLACK)
        self.screen.blit(progress_text, (50, 80))
    
    def draw_ui(self):
        """Draw the game UI"""
        # Energy bar
        energy_text = self.small_font.render("Energy:", True, self.BLACK)
        self.screen.blit(energy_text, (10, 10))
        
        energy_bar_width = 150
        energy_bar_height = 20
        pygame.draw.rect(self.screen, self.RED, (10, 35, energy_bar_width, energy_bar_height))
        pygame.draw.rect(self.screen, self.GREEN, (10, 35, 
                       int(energy_bar_width * self.player_energy / self.max_energy), energy_bar_height))
        pygame.draw.rect(self.screen, self.BLACK, (10, 35, energy_bar_width, energy_bar_height), 2)
        
        # Stats
        score_text = self.small_font.render(f"Score: {self.score}", True, self.BLACK)
        quests_text = self.small_font.render(f"Quests: {self.completed_quests}/{len(self.friends)}", True, self.BLACK)
        friends_text = self.small_font.render(f"Friends Helped: {len(self.completed_friends)}", True, self.BLACK)
        
        self.screen.blit(score_text, (10, 70))
        self.screen.blit(quests_text, (10, 95))
        self.screen.blit(friends_text, (10, 120))
        
        # Instructions
        instruction_text = self.small_font.render("Walk near friends to help them! WASD/Arrows to move", True, self.GRAY)
        self.screen.blit(instruction_text, (10, self.HEIGHT - 30))
    
    def draw_game_over(self):
        """Draw game over screen"""
        title = self.font.render("Game Over!", True, self.RED)
        score_text = self.small_font.render(f"Final Score: {self.score}", True, self.BLACK)
        instruction = self.small_font.render("Press R to restart or Q to quit", True, self.BLACK)
        
        title_rect = title.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 - 50))
        score_rect = score_text.get_rect(center=(self.WIDTH//2, self.HEIGHT//2))
        instruction_rect = instruction.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 + 50))
        
        self.screen.blit(title, title_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(instruction, instruction_rect)
    
    def draw_victory(self):
        """Draw victory screen"""
        title = self.font.render("Congratulations!", True, self.GREEN)
        subtitle = self.small_font.render("You helped all your friends!", True, self.BLACK)
        score_text = self.small_font.render(f"Final Score: {self.score}", True, self.BLACK)
        instruction = self.small_font.render("Press R to play again or Q to quit", True, self.BLACK)
        
        title_rect = title.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 - 75))
        subtitle_rect = subtitle.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 - 25))
        score_rect = score_text.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 + 25))
        instruction_rect = instruction.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 + 75))
        
        self.screen.blit(title, title_rect)
        self.screen.blit(subtitle, subtitle_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(instruction, instruction_rect)
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = QuestGame()
    game.run()
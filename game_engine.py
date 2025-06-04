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
        """Set up mini-game based on friend's specific objectives"""
        friend_name = self.current_friend.name
        objective = self.current_quest.get_objective().lower()
        
        # Specific mini-games for each friend's real objectives
        if friend_name == "Phrits":
            self.setup_biodiversity_game(objective)
        elif friend_name == "Mika":
            self.setup_sports_analysis_game(objective)
        elif friend_name == "Jordy":
            self.setup_mystery_disguise_game(objective)
        elif friend_name == "Casper":
            self.setup_wordplay_game(objective)
        elif friend_name == "Roel":
            self.setup_farming_game(objective)
        elif friend_name == "Alex":
            self.setup_innovation_game(objective)
        elif friend_name == "Rick":
            self.setup_mechanical_game(objective)
        elif friend_name == "Suen":
            self.setup_hacking_game(objective)
        else:
            # Fallback
            self.mini_game_type = 'button_mash'
            self.mini_game_progress = 0
            self.mini_game_target = 100
            self.mini_game_time = 0
            self.mini_game_duration = 5.0
    
    def setup_biodiversity_game(self, objective):
        """Phrits - Biodiversity exploration and specimen collection"""
        if "plant" in objective or "specimen" in objective:
            self.mini_game_type = 'specimen_collection'
            self.mini_game_instruction = "Collect rare specimens! Press SPACE when you see plants!"
        elif "forest" in objective or "explore" in objective:
            self.mini_game_type = 'forest_exploration'
            self.mini_game_instruction = "Navigate the forest! Use SPACE to move carefully!"
        elif "microorganism" in objective or "analyze" in objective:
            self.mini_game_type = 'microscope_analysis'
            self.mini_game_instruction = "Focus the microscope! Press SPACE at the right moment!"
        else:
            self.mini_game_type = 'fitness_challenge'
            self.mini_game_instruction = "Complete the fitness challenge! Rapid SPACE presses!"
        
        self.mini_game_progress = 0
        self.mini_game_target = 100
        self.mini_game_time = 0
        self.mini_game_duration = 6.0
        self.specimens_found = 0

    def setup_sports_analysis_game(self, objective):
        """Mika - Sports statistics and coaching"""
        if "statistic" in objective or "analyze" in objective:
            self.mini_game_type = 'stats_analysis'
            self.mini_game_instruction = "Analyze the data patterns! Press SPACE when numbers align!"
        elif "tournament" in objective or "win" in objective:
            self.mini_game_type = 'tournament_strategy'
            self.mini_game_instruction = "Make strategic decisions! Time your SPACE presses!"
        elif "coach" in objective:
            self.mini_game_type = 'team_coaching'
            self.mini_game_instruction = "Guide your team! Press SPACE to give instructions!"
        else:
            self.mini_game_type = 'trivia_challenge'
            self.mini_game_instruction = "Answer sports trivia! Quick SPACE presses for correct answers!"
        
        self.mini_game_progress = 0
        self.mini_game_target = 100
        self.mini_game_time = 0
        self.mini_game_duration = 7.0
        self.correct_answers = 0

    def setup_mystery_disguise_game(self, objective):
        """Jordy - Mystery solving and disguise mastery"""
        if "disguise" in objective or "art" in objective:
            self.mini_game_type = 'disguise_mastery'
            self.mini_game_instruction = "Perfect your disguise! Hold SPACE to blend in!"
        elif "mystery" in objective or "solve" in objective:
            self.mini_game_type = 'mystery_solving'
            self.mini_game_instruction = "Gather clues! Press SPACE to investigate!"
        elif "relationship" in objective:
            self.mini_game_type = 'relationship_counseling'
            self.mini_game_instruction = "Help resolve conflicts! Press SPACE at the right moments!"
        else:
            self.mini_game_type = 'car_show_organization'
            self.mini_game_instruction = "Organize the perfect car show! Precise SPACE timing!"
        
        self.mini_game_progress = 0
        self.mini_game_target = 100
        self.mini_game_time = 0
        self.mini_game_duration = 6.5
        self.stealth_meter = 50

    def setup_wordplay_game(self, objective):
        """Casper - Jokes, puns, and wordplay"""
        if "joke" in objective or "funny" in objective:
            self.mini_game_type = 'joke_telling'
            self.mini_game_instruction = "Time your punchlines! Press SPACE for perfect comedy timing!"
        elif "pun" in objective or "wordplay" in objective:
            self.mini_game_type = 'pun_battle'
            self.mini_game_instruction = "Create puns! Rapid SPACE presses for wordplay combos!"
        elif "riddle" in objective or "puzzle" in objective:
            self.mini_game_type = 'riddle_creation'
            self.mini_game_instruction = "Craft clever riddles! Press SPACE to build word puzzles!"
        else:
            self.mini_game_type = 'confusion_tactics'
            self.mini_game_instruction = "Confuse with wit! Random SPACE patterns!"
        
        self.mini_game_progress = 0
        self.mini_game_target = 100
        self.mini_game_time = 0
        self.mini_game_duration = 5.5
        self.comedy_meter = 0

    def setup_farming_game(self, objective):
        """Roel - Farming and cow care"""
        if "cow" in objective or "care" in objective:
            self.mini_game_type = 'cow_care'
            self.mini_game_instruction = "Take care of the cows! Gentle SPACE presses for feeding!"
        elif "harvest" in objective or "cultivate" in objective:
            self.mini_game_type = 'crop_harvesting'
            self.mini_game_instruction = "Harvest the crops! Rhythmic SPACE presses!"
        elif "wisdom" in objective or "farming" in objective:
            self.mini_game_type = 'farming_wisdom'
            self.mini_game_instruction = "Share farming knowledge! Press SPACE to teach!"
        else:
            self.mini_game_type = 'barnyard_party'
            self.mini_game_instruction = "Host the perfect gathering! Well-timed SPACE presses!"
        
        self.mini_game_progress = 0
        self.mini_game_target = 100
        self.mini_game_time = 0
        self.mini_game_duration = 6.0
        self.farm_happiness = 50

    def setup_innovation_game(self, objective):
        """Alex - Creative inventions and AI knowledge"""
        if "invention" in objective or "create" in objective:
            self.mini_game_type = 'invention_workshop'
            self.mini_game_instruction = "Build amazing inventions! Creative SPACE combinations!"
        elif "story" in objective or "craft" in objective:
            self.mini_game_type = 'story_crafting'
            self.mini_game_instruction = "Craft hilarious stories! Press SPACE to add plot twists!"
        elif "ai" in objective or "knowledge" in objective:
            self.mini_game_type = 'ai_exploration'
            self.mini_game_instruction = "Explore AI concepts! Precise SPACE timing for learning!"
        else:
            self.mini_game_type = 'creative_workshop'
            self.mini_game_instruction = "Lead creative workshops! Inspiring SPACE presses!"
        
        self.mini_game_progress = 0
        self.mini_game_target = 100
        self.mini_game_time = 0
        self.mini_game_duration = 7.0
        self.creativity_sparks = 0

    def setup_mechanical_game(self, objective):
        """Rick - Mechanical fixes and technical solutions"""
        if "fix" in objective or "broken" in objective:
            self.mini_game_type = 'machinery_repair'
            self.mini_game_instruction = "Fix the machinery! Precise SPACE presses for repairs!"
        elif "technical" in objective or "solution" in objective:
            self.mini_game_type = 'technical_problem_solving'
            self.mini_game_instruction = "Solve technical challenges! Strategic SPACE timing!"
        elif "firework" in objective or "safely" in objective:
            self.mini_game_type = 'fireworks_safety'
            self.mini_game_instruction = "Handle fireworks safely! Careful SPACE timing!"
        else:
            self.mini_game_type = 'mechanical_workshop'
            self.mini_game_instruction = "Teach mechanical skills! Educational SPACE presses!"
        
        self.mini_game_progress = 0
        self.mini_game_target = 100
        self.mini_game_time = 0
        self.mini_game_duration = 6.5
        self.precision_level = 0

    def setup_hacking_game(self, objective):
        """Suen - Gaming, hacking, and optimization"""
        if "virtual" in objective or "realm" in objective:
            self.mini_game_type = 'virtual_mastery'
            self.mini_game_instruction = "Master virtual realms! Complex SPACE patterns!"
        elif "hacking" in objective or "challenge" in objective:
            self.mini_game_type = 'hacking_challenge'
            self.mini_game_instruction = "Hack the system! Precise SPACE sequences!"
        elif "score" in objective or "high" in objective:
            self.mini_game_type = 'high_score_chase'
            self.mini_game_instruction = "Achieve high scores! Perfect SPACE timing!"
        else:
            self.mini_game_type = 'lan_party_hosting'
            self.mini_game_instruction = "Host epic game nights! Coordinated SPACE presses!"
        
        self.mini_game_progress = 0
        self.mini_game_target = 100
        self.mini_game_time = 0
        self.mini_game_duration = 6.0
        self.hack_success = 0
    
    def update_mini_game(self):
        """Update mini-game logic based on specific game type"""
        self.mini_game_time += 1/self.FPS
        
        # Specific mechanics for each friend's mini-games
        if self.mini_game_type in ['specimen_collection', 'forest_exploration']:
            # Phrits games - environmental progression
            if random.random() < 0.03:  # Random discoveries
                self.mini_game_progress += 8
                self.specimens_found += 1
        
        elif self.mini_game_type in ['stats_analysis', 'tournament_strategy']:
            # Mika games - analytical progression
            if int(self.mini_game_time * 3) % 4 == 0:  # Pattern-based
                self.mini_game_progress += 0.3
        
        elif self.mini_game_type in ['disguise_mastery', 'mystery_solving']:
            # Jordy games - stealth mechanics
            self.stealth_meter += random.uniform(-1, 1)
            self.stealth_meter = max(0, min(100, self.stealth_meter))
            if self.stealth_meter > 70:
                self.mini_game_progress += 0.8
        
        elif self.mini_game_type in ['joke_telling', 'pun_battle']:
            # Casper games - comedy timing
            if int(self.mini_game_time * 4) % 3 == 0:  # Comedy rhythm
                self.comedy_meter += 2
                self.mini_game_progress += 0.4
        
        elif self.mini_game_type in ['cow_care', 'crop_harvesting']:
            # Roel games - farming progression
            self.farm_happiness += random.uniform(-0.5, 1.5)
            self.farm_happiness = max(0, min(100, self.farm_happiness))
            if self.farm_happiness > 60:
                self.mini_game_progress += 0.6
        
        elif self.mini_game_type in ['invention_workshop', 'story_crafting']:
            # Alex games - creative bursts
            if random.random() < 0.05:  # Inspiration moments
                self.creativity_sparks += 1
                self.mini_game_progress += 12
        
        elif self.mini_game_type in ['machinery_repair', 'fireworks_safety']:
            # Rick games - precision requirements
            self.precision_level += random.uniform(-2, 1)
            self.precision_level = max(0, min(100, self.precision_level))
            # Only progress with good precision
            if self.precision_level > 50:
                self.mini_game_progress += 0.3
        
        elif self.mini_game_type in ['hacking_challenge', 'virtual_mastery']:
            # Suen games - technical complexity
            if int(self.mini_game_time * 6) % 7 == 0:  # Complex patterns
                self.hack_success += 1
                self.mini_game_progress += 0.5
        
        # Generic progress for other games
        else:
            if random.random() < 0.02:
                self.mini_game_progress += 1
        
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
        
        # Show specific instruction for this mini-game
        instruction_text = getattr(self, 'mini_game_instruction', "Press SPACE to help!")
        instruction = self.small_font.render(instruction_text, True, self.BLACK)
        instruction_rect = instruction.get_rect(center=(self.WIDTH//2, 400))
        self.screen.blit(instruction, instruction_rect)
        
        # Timer
        time_left = max(0, self.mini_game_duration - self.mini_game_time)
        timer_text = self.small_font.render(f"Time: {time_left:.1f}s", True, self.BLACK)
        self.screen.blit(timer_text, (50, 50))
        
        # Progress text
        progress_text = self.small_font.render(f"Progress: {int(self.mini_game_progress)}/{self.mini_game_target}", True, self.BLACK)
        self.screen.blit(progress_text, (50, 80))
        
        # Draw specific game context visuals
        self.draw_mini_game_context()
    
    def draw_mini_game_context(self):
        """Draw visual context for specific mini-games"""
        y_pos = 450
        
        # Phrits games - nature context
        if self.mini_game_type in ['specimen_collection', 'forest_exploration', 'microscope_analysis']:
            context_text = f"🌱 Specimens Found: {getattr(self, 'specimens_found', 0)}"
            if self.mini_game_type == 'microscope_analysis':
                context_text = "🔬 Analyzing microorganisms..."
            elif self.mini_game_type == 'forest_exploration':
                context_text = "🌲 Exploring the forest depths..."
        
        # Mika games - sports context
        elif self.mini_game_type in ['stats_analysis', 'tournament_strategy', 'team_coaching']:
            context_text = f"📊 Correct Analysis: {getattr(self, 'correct_answers', 0)}"
            if self.mini_game_type == 'tournament_strategy':
                context_text = "🏆 Planning tournament strategy..."
            elif self.mini_game_type == 'team_coaching':
                context_text = "👥 Coaching the team to victory..."
        
        # Jordy games - mystery context
        elif self.mini_game_type in ['disguise_mastery', 'mystery_solving', 'relationship_counseling']:
            stealth = getattr(self, 'stealth_meter', 50)
            context_text = f"🎭 Stealth Level: {int(stealth)}/100"
            if self.mini_game_type == 'mystery_solving':
                context_text = "🔍 Gathering clues and evidence..."
            elif self.mini_game_type == 'relationship_counseling':
                context_text = "💝 Helping resolve relationship issues..."
        
        # Casper games - comedy context
        elif self.mini_game_type in ['joke_telling', 'pun_battle', 'riddle_creation']:
            comedy = getattr(self, 'comedy_meter', 0)
            context_text = f"😂 Comedy Power: {int(comedy)}"
            if self.mini_game_type == 'pun_battle':
                context_text = "🎯 Crafting devastating puns..."
            elif self.mini_game_type == 'riddle_creation':
                context_text = "🧩 Creating mind-bending riddles..."
        
        # Roel games - farming context
        elif self.mini_game_type in ['cow_care', 'crop_harvesting', 'farming_wisdom']:
            happiness = getattr(self, 'farm_happiness', 50)
            context_text = f"🐄 Farm Happiness: {int(happiness)}/100"
            if self.mini_game_type == 'crop_harvesting':
                context_text = "🌾 Harvesting bountiful crops..."
            elif self.mini_game_type == 'farming_wisdom':
                context_text = "📚 Sharing agricultural wisdom..."
        
        # Alex games - creative context
        elif self.mini_game_type in ['invention_workshop', 'story_crafting', 'ai_exploration']:
            sparks = getattr(self, 'creativity_sparks', 0)
            context_text = f"💡 Creative Sparks: {sparks}"
            if self.mini_game_type == 'story_crafting':
                context_text = "📖 Crafting hilarious stories..."
            elif self.mini_game_type == 'ai_exploration':
                context_text = "🤖 Exploring AI concepts..."
        
        # Rick games - technical context
        elif self.mini_game_type in ['machinery_repair', 'technical_problem_solving', 'fireworks_safety']:
            precision = getattr(self, 'precision_level', 0)
            context_text = f"🔧 Precision: {int(precision)}/100"
            if self.mini_game_type == 'fireworks_safety':
                context_text = "🎆 Handling fireworks with care..."
            elif self.mini_game_type == 'technical_problem_solving':
                context_text = "⚙️ Solving complex technical issues..."
        
        # Suen games - hacking context
        elif self.mini_game_type in ['hacking_challenge', 'virtual_mastery', 'high_score_chase']:
            success = getattr(self, 'hack_success', 0)
            context_text = f"💻 Systems Hacked: {success}"
            if self.mini_game_type == 'virtual_mastery':
                context_text = "🌐 Mastering virtual realms..."
            elif self.mini_game_type == 'high_score_chase':
                context_text = "🎮 Chasing the ultimate high score..."
        
        else:
            context_text = "🎯 Working together..."
        
        # Render and display the context
        context_surface = self.small_font.render(context_text, True, self.BLACK)
        context_rect = context_surface.get_rect(center=(self.WIDTH//2, y_pos))
        self.screen.blit(context_surface, context_rect)
    
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
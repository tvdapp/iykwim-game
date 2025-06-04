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
        
        # Specific mini-game data
        self.plant_positions = []
        self.selected_plant = None
        self.correct_plants = 0
        self.mouse_pos = (0, 0)
        
        # Sports analysis game
        self.stats_pattern = []
        self.player_pattern = []
        self.current_stat = 0
        
        # Mystery game
        self.clues = []
        self.found_clues = []
        self.mystery_grid = []
        
        # Joke game
        self.joke_words = []
        self.current_joke = ""
        self.joke_timing = 0
        
        # Farming game  
        self.cows = []
        self.cow_happiness = []
        self.feed_level = 50
        
        # Invention game
        self.invention_parts = []
        self.connected_parts = []
        self.circuit_complete = False
        
        # Mechanical game
        self.broken_parts = []
        self.fixed_parts = []
        self.tool_selected = None
        
        # Hacking game
        self.code_sequence = []
        self.player_sequence = []
        self.hack_grid = []
        
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
                    self.handle_mini_game_input(event)
                elif self.state in [GameState.GAME_OVER, GameState.VICTORY]:
                    if event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_q:
                        self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == GameState.MINI_GAME:
                    self.handle_mini_game_mouse(event)
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
    
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
        """Phrits - Plant Collection - Click on plants to collect them"""
        self.mini_game_type = 'plant_collection'
        self.mini_game_instruction = "Click on the rare plants to collect them!"
        
        # Create random plant positions
        self.plant_positions = []
        for _ in range(8):
            x = random.randint(100, self.WIDTH - 100)
            y = random.randint(200, 500)
            plant_type = random.choice(['🌿', '🍄', '🌺', '🌻', '🌱'])
            self.plant_positions.append({'x': x, 'y': y, 'type': plant_type, 'collected': False})
        
        self.mini_game_progress = 0
        self.mini_game_target = 6  # Collect 6 plants
        self.mini_game_time = 0
        self.mini_game_duration = 10.0
        self.specimens_found = 0

    def setup_sports_analysis_game(self, objective):
        """Mika - Pattern Matching - Match the statistical patterns"""
        self.mini_game_type = 'pattern_matching'
        self.mini_game_instruction = "Match the statistical pattern! Press 1-4 keys to match the sequence!"
        
        # Create a pattern sequence 
        self.stats_pattern = [random.randint(1, 4) for _ in range(6)]
        self.player_pattern = []
        self.current_stat = 0
        
        self.mini_game_progress = 0
        self.mini_game_target = 5  # Complete 5 patterns
        self.mini_game_time = 0
        self.mini_game_duration = 15.0
        self.correct_answers = 0

    def setup_mystery_disguise_game(self, objective):
        """Jordy - Memory Card Matching - Find matching clue pairs"""
        self.mini_game_type = 'memory_cards'
        self.mini_game_instruction = "Click cards to find matching clue pairs!"
        
        # Create memory card grid (4x4)
        clue_symbols = ['🔍', '🗝️', '📄', '👤', '🎭', '🚗', '💎', '🔮']
        all_cards = clue_symbols + clue_symbols  # Pairs
        random.shuffle(all_cards)
        
        self.mystery_grid = []
        for i in range(4):
            row = []
            for j in range(4):
                card = {
                    'symbol': all_cards[i*4 + j],
                    'revealed': False,
                    'matched': False,
                    'x': 300 + j * 70,
                    'y': 250 + i * 70
                }
                row.append(card)
            self.mystery_grid.append(row)
        
        self.revealed_cards = []
        self.mini_game_progress = 0
        self.mini_game_target = 8  # Match all 8 pairs
        self.mini_game_time = 0
        self.mini_game_duration = 20.0

    def setup_wordplay_game(self, objective):
        """Casper - Word Completion - Complete the jokes by typing missing words"""
        self.mini_game_type = 'word_completion'
        self.mini_game_instruction = "Type the missing word to complete the joke!"
        
        # Joke templates with missing words
        self.joke_templates = [
            ("Why don't scientists trust atoms? Because they make up everything and they're always ___!", "lying"),
            ("What do you call a fake noodle? An ___!", "impasta"),
            ("Why did the scarecrow win an award? He was outstanding in his ___!", "field"),
            ("What do you call a bear with no teeth? A ___ bear!", "gummy"),
            ("Why don't eggs tell jokes? They'd ___!", "crack"),
        ]
        
        self.current_joke_index = 0
        self.current_answer = ""
        self.typed_answer = ""
        
        self.mini_game_progress = 0
        self.mini_game_target = 3  # Complete 3 jokes
        self.mini_game_time = 0
        self.mini_game_duration = 20.0

    def setup_farming_game(self, objective):
        """Roel - Cow Feeding - Move mouse to feed the cows"""
        self.mini_game_type = 'cow_feeding'
        self.mini_game_instruction = "Move your mouse near the cows to feed them!"
        
        # Create cow positions and happiness levels
        self.cows = []
        for i in range(5):
            cow = {
                'x': random.randint(100, self.WIDTH - 100),
                'y': random.randint(300, 500),
                'happiness': random.randint(30, 70),
                'fed': False,
                'last_feed_time': 0
            }
            self.cows.append(cow)
        
        self.feed_radius = 80
        self.mini_game_progress = 0
        self.mini_game_target = 5  # Feed all 5 cows to happiness > 90
        self.mini_game_time = 0
        self.mini_game_duration = 15.0

    def setup_innovation_game(self, objective):
        """Alex - Circuit Building - Connect invention parts by clicking them"""
        self.mini_game_type = 'circuit_building'
        self.mini_game_instruction = "Click parts to connect them and complete the invention!"
        
        # Create invention parts that need to be connected
        part_types = ['💡', '🔧', '⚙️', '🔋', '📡', '🖥️']
        self.invention_parts = []
        for i, part_type in enumerate(part_types):
            part = {
                'type': part_type,
                'x': 200 + (i % 3) * 150,
                'y': 300 + (i // 3) * 100,
                'connected': False,
                'id': i
            }
            self.invention_parts.append(part)
        
        self.connection_order = list(range(len(part_types)))
        random.shuffle(self.connection_order)
        self.current_connection = 0
        
        self.mini_game_progress = 0
        self.mini_game_target = 6  # Connect all 6 parts in order
        self.mini_game_time = 0
        self.mini_game_duration = 18.0

    def setup_mechanical_game(self, objective):
        """Rick - Tool Selection - Choose the right tools for broken parts"""
        self.mini_game_type = 'tool_selection'
        self.mini_game_instruction = "Click the right tool for each broken part!"
        
        # Create broken parts and corresponding tools
        self.broken_parts = [
            {'part': '🔩', 'tool': '🔧', 'x': 200, 'y': 300, 'fixed': False},
            {'part': '⚡', 'tool': '🪛', 'x': 350, 'y': 300, 'fixed': False},
            {'part': '🔌', 'tool': '✂️', 'x': 500, 'y': 300, 'fixed': False},
            {'part': '⚙️', 'tool': '🔨', 'x': 650, 'y': 300, 'fixed': False},
        ]
        
        self.available_tools = ['🔧', '🪛', '✂️', '🔨', '📏', '🪚']
        random.shuffle(self.available_tools)
        self.selected_tool = None
        
        self.mini_game_progress = 0
        self.mini_game_target = 4  # Fix all 4 parts
        self.mini_game_time = 0
        self.mini_game_duration = 15.0

    def setup_hacking_game(self, objective):
        """Suen - Code Sequence - Enter the correct arrow key sequences"""
        self.mini_game_type = 'code_sequence'
        self.mini_game_instruction = "Enter the arrow key sequences shown! ↑↓←→"
        
        # Create code sequences using arrow keys
        self.code_sequences = []
        arrow_keys = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        
        for _ in range(5):
            sequence = [random.choice(arrow_keys) for _ in range(4)]
            self.code_sequences.append({
                'sequence': sequence,
                'current_input': [],
                'completed': False,
                'display_time': 3.0  # Show sequence for 3 seconds
            })
        
        self.current_sequence_index = 0
        self.sequence_display_timer = 0
        self.showing_sequence = True
        
        self.mini_game_progress = 0
        self.mini_game_target = 5  # Complete all 5 sequences
        self.mini_game_time = 0
        self.mini_game_duration = 25.0
    
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
        
        # Update specific mini-game mechanics
        if self.mini_game_type == 'cow_feeding':
            # Update cow feeding with mouse proximity
            for cow in self.cows:
                if not cow['fed']:
                    distance = math.sqrt((self.mouse_pos[0] - cow['x'])**2 + (self.mouse_pos[1] - cow['y'])**2)
                    if distance < self.feed_radius:
                        cow['happiness'] = min(100, cow['happiness'] + 1)
                        if cow['happiness'] >= 90:
                            cow['fed'] = True
                            self.mini_game_progress += 1
        
        elif self.mini_game_type == 'code_sequence':
            # Handle sequence display timing
            if self.showing_sequence:
                self.sequence_display_timer += 1/self.FPS
                if self.sequence_display_timer >= 3.0:
                    self.showing_sequence = False
                    self.sequence_display_timer = 0
        
        # Check mini-game completion
        if self.mini_game_time >= self.mini_game_duration:
            self.complete_mini_game()
        elif self.mini_game_progress >= self.mini_game_target:
            self.complete_mini_game()
        elif self.mini_game_progress < 0:
            self.fail_mini_game()
    
    def handle_mini_game_input(self, event):
        """Handle keyboard input for mini-games"""
        if self.mini_game_type == 'pattern_matching':
            # Mika's pattern matching - number keys 1-4
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                number = event.key - pygame.K_0
                self.player_pattern.append(number)
                
                # Check if pattern matches so far
                if len(self.player_pattern) <= len(self.stats_pattern):
                    if self.player_pattern[-1] == self.stats_pattern[len(self.player_pattern)-1]:
                        # Correct so far
                        if len(self.player_pattern) == len(self.stats_pattern):
                            # Pattern complete!
                            self.mini_game_progress += 1
                            self.correct_answers += 1
                            # Generate new pattern
                            self.stats_pattern = [random.randint(1, 4) for _ in range(6)]
                            self.player_pattern = []
                    else:
                        # Wrong! Reset
                        self.player_pattern = []
        
        elif self.mini_game_type == 'word_completion':
            # Casper's word completion - type letters
            if event.unicode.isalpha():
                self.typed_answer += event.unicode.lower()
            elif event.key == pygame.K_BACKSPACE:
                self.typed_answer = self.typed_answer[:-1]
            elif event.key == pygame.K_RETURN:
                # Check answer
                if self.current_joke_index < len(self.joke_templates):
                    correct_answer = self.joke_templates[self.current_joke_index][1].lower()
                    if self.typed_answer.lower() == correct_answer:
                        self.mini_game_progress += 1
                        self.current_joke_index += 1
                        self.typed_answer = ""
                    else:
                        self.typed_answer = ""
        
        elif self.mini_game_type == 'code_sequence':
            # Suen's code sequence - arrow keys
            if not self.showing_sequence and self.current_sequence_index < len(self.code_sequences):
                current_seq = self.code_sequences[self.current_sequence_index]
                
                key_map = {
                    pygame.K_UP: 'UP',
                    pygame.K_DOWN: 'DOWN', 
                    pygame.K_LEFT: 'LEFT',
                    pygame.K_RIGHT: 'RIGHT'
                }
                
                if event.key in key_map:
                    current_seq['current_input'].append(key_map[event.key])
                    
                    # Check if sequence is correct so far
                    if len(current_seq['current_input']) <= len(current_seq['sequence']):
                        if (current_seq['current_input'][-1] == 
                            current_seq['sequence'][len(current_seq['current_input'])-1]):
                            # Correct so far
                            if len(current_seq['current_input']) == len(current_seq['sequence']):
                                # Sequence complete!
                                current_seq['completed'] = True
                                self.mini_game_progress += 1
                                self.current_sequence_index += 1
                                self.showing_sequence = True
                                self.sequence_display_timer = 0
                        else:
                            # Wrong! Reset
                            current_seq['current_input'] = []
    
    def handle_mini_game_mouse(self, event):
        """Handle mouse clicks for mini-games"""
        mouse_x, mouse_y = event.pos
        
        if self.mini_game_type == 'plant_collection':
            # Phrits' plant collection - click plants
            for plant in self.plant_positions:
                if not plant['collected']:
                    distance = math.sqrt((mouse_x - plant['x'])**2 + (mouse_y - plant['y'])**2)
                    if distance < 30:  # Click radius
                        plant['collected'] = True
                        self.mini_game_progress += 1
                        self.specimens_found += 1
        
        elif self.mini_game_type == 'memory_cards':
            # Jordy's memory cards - click cards
            for row in self.mystery_grid:
                for card in row:
                    if (mouse_x >= card['x'] and mouse_x <= card['x'] + 60 and
                        mouse_y >= card['y'] and mouse_y <= card['y'] + 60):
                        if not card['revealed'] and not card['matched']:
                            card['revealed'] = True
                            self.revealed_cards.append(card)
                            
                            if len(self.revealed_cards) == 2:
                                # Check for match
                                if (self.revealed_cards[0]['symbol'] == 
                                    self.revealed_cards[1]['symbol']):
                                    # Match found!
                                    for revealed_card in self.revealed_cards:
                                        revealed_card['matched'] = True
                                    self.mini_game_progress += 1
                                else:
                                    # No match, hide cards after delay
                                    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
                                self.revealed_cards = []
        
        elif self.mini_game_type == 'circuit_building':
            # Alex's circuit building - click parts in order
            for part in self.invention_parts:
                if (mouse_x >= part['x'] and mouse_x <= part['x'] + 50 and
                    mouse_y >= part['y'] and mouse_y <= part['y'] + 50):
                    if not part['connected']:
                        expected_id = self.connection_order[self.current_connection]
                        if part['id'] == expected_id:
                            part['connected'] = True
                            self.current_connection += 1
                            self.mini_game_progress += 1
                        else:
                            # Wrong part, reset
                            for p in self.invention_parts:
                                p['connected'] = False
                            self.current_connection = 0
                            self.mini_game_progress = 0
        
        elif self.mini_game_type == 'tool_selection':
            # Rick's tool selection - click tools then parts
            # First check if clicking a tool
            for i, tool in enumerate(self.available_tools):
                tool_x = 200 + i * 80
                tool_y = 450
                if (mouse_x >= tool_x and mouse_x <= tool_x + 60 and
                    mouse_y >= tool_y and mouse_y <= tool_y + 60):
                    self.selected_tool = tool
                    return
            
            # Then check if clicking a broken part with selected tool
            if self.selected_tool:
                for part in self.broken_parts:
                    if not part['fixed']:
                        if (mouse_x >= part['x'] and mouse_x <= part['x'] + 60 and
                            mouse_y >= part['y'] and mouse_y <= part['y'] + 60):
                            if self.selected_tool == part['tool']:
                                part['fixed'] = True
                                self.mini_game_progress += 1
                                self.selected_tool = None
                            else:
                                # Wrong tool, deselect
                                self.selected_tool = None
    
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
        """Draw the actual mini-game interface"""
        if self.mini_game_type == 'plant_collection':
            # Draw plants to collect
            for plant in self.plant_positions:
                if not plant['collected']:
                    # Draw plant
                    plant_surface = self.font.render(plant['type'], True, self.BLACK)
                    plant_rect = plant_surface.get_rect(center=(plant['x'], plant['y']))
                    self.screen.blit(plant_surface, plant_rect)
                    # Draw collection circle
                    pygame.draw.circle(self.screen, self.GREEN, (plant['x'], plant['y']), 25, 2)
        
        elif self.mini_game_type == 'pattern_matching':
            # Draw the pattern to match
            pattern_text = "Pattern: " + " ".join([str(x) for x in self.stats_pattern])
            pattern_surface = self.small_font.render(pattern_text, True, self.BLACK)
            self.screen.blit(pattern_surface, (50, 450))
            
            # Draw player's current input
            input_text = "Input: " + " ".join([str(x) for x in self.player_pattern])
            input_surface = self.small_font.render(input_text, True, self.BLUE)
            self.screen.blit(input_surface, (50, 480))
            
            # Draw number buttons
            for i in range(1, 5):
                button_x = 300 + i * 80
                button_y = 350
                pygame.draw.rect(self.screen, self.LIGHT_GRAY, (button_x, button_y, 60, 60))
                pygame.draw.rect(self.screen, self.BLACK, (button_x, button_y, 60, 60), 2)
                number_surface = self.font.render(str(i), True, self.BLACK)
                number_rect = number_surface.get_rect(center=(button_x + 30, button_y + 30))
                self.screen.blit(number_surface, number_rect)
        
        elif self.mini_game_type == 'memory_cards':
            # Draw memory card grid
            for row in self.mystery_grid:
                for card in row:
                    # Card background
                    card_color = self.GREEN if card['matched'] else self.LIGHT_GRAY
                    pygame.draw.rect(self.screen, card_color, (card['x'], card['y'], 60, 60))
                    pygame.draw.rect(self.screen, self.BLACK, (card['x'], card['y'], 60, 60), 2)
                    
                    # Card content
                    if card['revealed'] or card['matched']:
                        symbol_surface = self.font.render(card['symbol'], True, self.BLACK)
                        symbol_rect = symbol_surface.get_rect(center=(card['x'] + 30, card['y'] + 30))
                        self.screen.blit(symbol_surface, symbol_rect)
                    else:
                        # Hidden card
                        pygame.draw.rect(self.screen, self.GRAY, (card['x'] + 5, card['y'] + 5, 50, 50))
        
        elif self.mini_game_type == 'word_completion':
            # Draw current joke
            if self.current_joke_index < len(self.joke_templates):
                joke, answer = self.joke_templates[self.current_joke_index]
                joke_surface = self.small_font.render(joke, True, self.BLACK)
                joke_rect = joke_surface.get_rect(center=(self.WIDTH//2, 350))
                self.screen.blit(joke_surface, joke_rect)
                
                # Draw typed answer
                answer_text = f"Your answer: {self.typed_answer}"
                answer_surface = self.small_font.render(answer_text, True, self.BLUE)
                answer_rect = answer_surface.get_rect(center=(self.WIDTH//2, 400))
                self.screen.blit(answer_surface, answer_rect)
        
        elif self.mini_game_type == 'cow_feeding':
            # Draw cows
            for cow in self.cows:
                # Cow emoji
                cow_surface = self.font.render('🐄', True, self.BLACK)
                cow_rect = cow_surface.get_rect(center=(cow['x'], cow['y']))
                self.screen.blit(cow_surface, cow_rect)
                
                # Happiness bar
                bar_width = 60
                bar_height = 8
                bar_x = cow['x'] - bar_width // 2
                bar_y = cow['y'] - 40
                
                pygame.draw.rect(self.screen, self.RED, (bar_x, bar_y, bar_width, bar_height))
                pygame.draw.rect(self.screen, self.GREEN, (bar_x, bar_y, 
                               int(bar_width * cow['happiness'] / 100), bar_height))
                
                # Feeding radius
                if not cow['fed']:
                    distance = math.sqrt((self.mouse_pos[0] - cow['x'])**2 + (self.mouse_pos[1] - cow['y'])**2)
                    if distance < self.feed_radius:
                        pygame.draw.circle(self.screen, (0, 255, 0, 50), (cow['x'], cow['y']), self.feed_radius, 2)
        
        elif self.mini_game_type == 'circuit_building':
            # Draw invention parts
            for part in self.invention_parts:
                part_color = self.GREEN if part['connected'] else self.LIGHT_GRAY
                pygame.draw.rect(self.screen, part_color, (part['x'], part['y'], 50, 50))
                pygame.draw.rect(self.screen, self.BLACK, (part['x'], part['y'], 50, 50), 2)
                
                part_surface = self.font.render(part['type'], True, self.BLACK)
                part_rect = part_surface.get_rect(center=(part['x'] + 25, part['y'] + 25))
                self.screen.blit(part_surface, part_rect)
            
            # Show connection order
            if self.current_connection < len(self.connection_order):
                next_part_id = self.connection_order[self.current_connection]
                order_text = f"Connect: {self.invention_parts[next_part_id]['type']}"
                order_surface = self.small_font.render(order_text, True, self.BLACK)
                self.screen.blit(order_surface, (50, 450))
        
        elif self.mini_game_type == 'tool_selection':
            # Draw available tools
            for i, tool in enumerate(self.available_tools):
                tool_x = 200 + i * 80
                tool_y = 450
                tool_color = self.BLUE if self.selected_tool == tool else self.LIGHT_GRAY
                pygame.draw.rect(self.screen, tool_color, (tool_x, tool_y, 60, 60))
                pygame.draw.rect(self.screen, self.BLACK, (tool_x, tool_y, 60, 60), 2)
                
                tool_surface = self.font.render(tool, True, self.BLACK)
                tool_rect = tool_surface.get_rect(center=(tool_x + 30, tool_y + 30))
                self.screen.blit(tool_surface, tool_rect)
            
            # Draw broken parts
            for part in self.broken_parts:
                part_color = self.GREEN if part['fixed'] else self.RED
                pygame.draw.rect(self.screen, part_color, (part['x'], part['y'], 60, 60))
                pygame.draw.rect(self.screen, self.BLACK, (part['x'], part['y'], 60, 60), 2)
                
                part_surface = self.font.render(part['part'], True, self.BLACK)
                part_rect = part_surface.get_rect(center=(part['x'] + 30, part['y'] + 30))
                self.screen.blit(part_surface, part_rect)
        
        elif self.mini_game_type == 'code_sequence':
            # Draw code sequence
            if self.current_sequence_index < len(self.code_sequences):
                current_seq = self.code_sequences[self.current_sequence_index]
                
                if self.showing_sequence:
                    # Show the sequence to memorize
                    sequence_text = "Memorize: " + " ".join(['↑' if x == 'UP' else '↓' if x == 'DOWN' else '←' if x == 'LEFT' else '→' for x in current_seq['sequence']])
                    sequence_surface = self.font.render(sequence_text, True, self.BLACK)
                    sequence_rect = sequence_surface.get_rect(center=(self.WIDTH//2, 350))
                    self.screen.blit(sequence_surface, sequence_rect)
                else:
                    # Show input prompt
                    input_text = "Enter sequence: " + " ".join(['↑' if x == 'UP' else '↓' if x == 'DOWN' else '←' if x == 'LEFT' else '→' for x in current_seq['current_input']])
                    input_surface = self.font.render(input_text, True, self.BLUE)
                    input_rect = input_surface.get_rect(center=(self.WIDTH//2, 350))
                    self.screen.blit(input_surface, input_rect)
    
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
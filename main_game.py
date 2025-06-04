#!/usr/bin/env python3
"""
IYKWIM: Friend Quest Adventure
A fun, interactive game where you help your friends complete their objectives!

Features:
- Explore and interact with 8 unique friends
- Each friend has special abilities and personal objectives
- Mini-games based on friend abilities (button mashing, precision, rhythm, etc.)
- Energy and friendship management
- Score system and progression
- Beautiful character sprites and animations

Controls:
- WASD or Arrow Keys: Move around
- Space: Interact in mini-games
- Y/N: Accept/Decline quests

How to Play:
1. Walk near friends (they glow when they have quests)
2. Talk to them to learn about their objectives
3. Accept their quest to start a mini-game
4. Complete mini-games to help friends and earn points
5. Help all friends to win the game!

Created by Thijs van Dam with AI assistance
"""

import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from game_engine import QuestGame
    print("🎮 IYKWIM: Friend Quest Adventure")
    print("=================================")
    print("Loading game...")
    
    # Create and run the game
    game = QuestGame()
    print("✅ Game loaded successfully!")
    print("💡 Tip: Walk near friends to help them with their objectives!")
    game.run()
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure all required modules are available:")
    print("- pygame")
    print("- All Abilities/*.py files")
    print("- All Colors/*.py files") 
    print("- All Objectives/*.py files")
    print("- Friend.py")
    print("\nTry: pip install pygame")
    
except FileNotFoundError as e:
    print(f"❌ File Error: {e}")
    print("Make sure all image files are in resources/cutout/:")
    print("- thijs.png (player)")
    print("- alex.png, casper.png, gurdy.png, mika.png")
    print("- phrits.png, pringers.png, roel.png, suenpai.png")
    
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
    print("Something went wrong! Check the error above.")
    
finally:
    print("\n👋 Thanks for playing IYKWIM: Friend Quest Adventure!")
    print("Created with ❤️ by Thijs van Dam")
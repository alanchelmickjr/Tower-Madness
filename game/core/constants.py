"""
Game constants for Tower Madness / Elevator Operator
Defines screen settings, colors, and floor configurations
"""

import pygame

# Screen settings for arcade cabinet
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
TITLE = "Tower Madness - Elevator Operator"

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GOLD = (255, 215, 0)

# Elevator colors
ELEVATOR_COLOR = (100, 100, 120)
ELEVATOR_DOOR_COLOR = (80, 80, 100)
CABLE_COLOR = (60, 60, 60)

# Floor colors and themes - Complete Frontier Tower Layout
FLOOR_COLORS = {
    -1: (150, 0, 0),      # Basement - Robot Fight Club (red theme)
    0: (100, 100, 100),   # Street Level (gray)
    1: (150, 150, 150),   # Lobby
    2: (100, 150, 200),   # Event Space "The Spaceship" (blue theme)
    3: (120, 120, 150),   # Private offices
    4: (0, 150, 255),     # Robotics Lab - Alan's command center (blue theme)
    5: (200, 150, 100),   # Gym/Movement (orange/brown for construction)
    6: (200, 100, 200),   # Arts & Music (purple/magenta)
    7: (150, 100, 50),    # Maker Space (brown/industrial)
    8: (100, 200, 100),   # Biotech Labs (green)
    9: (100, 100, 200),   # AI & Autonomous Systems (deep blue)
    10: (255, 215, 0),    # VCs and Accelerator (gold)
    11: (150, 255, 150),  # Health & Longevity (light green)
    12: (255, 165, 0),    # Crypto/DeFi (orange/bitcoin)
    14: (255, 200, 255),  # Human Flourishing (no 13th floor!) (light pink)
    15: (180, 180, 200),  # Coworking & Library (light gray-blue)
    16: (200, 0, 200),    # d/acc Lounge (magenta)
    17: (255, 0, 255),    # Roof - Secret Rave venue (bright magenta)
}

# Floor definitions with narrative elements - Complete Frontier Tower
FLOORS = {
    -1: {
        "name": "Basement - Robot Fight Club",
        "description": "Evil robots battle in red-lit cages (decoy/distraction)",
        "theme": "evil",
        "color": RED,
        "ambient_color": (100, 0, 0)
    },
    0: {
        "name": "Street Level",
        "description": "Ground floor entrance with John the doorman",
        "theme": "neutral",
        "color": GRAY,
        "ambient_color": (150, 150, 150)
    },
    1: {
        "name": "Floor 1 - Lobby",
        "description": "Main lobby and reception area",
        "theme": "neutral",
        "color": LIGHT_GRAY,
        "ambient_color": (180, 180, 180)
    },
    2: {
        "name": "Floor 2 - The Spaceship",
        "description": "Event space for launches and gatherings",
        "theme": "neutral",
        "color": (100, 150, 200),
        "ambient_color": (120, 170, 220)
    },
    3: {
        "name": "Floor 3 - Private Offices",
        "description": "Quiet workspace for focused work",
        "theme": "neutral",
        "color": (120, 120, 150),
        "ambient_color": (140, 140, 170)
    },
    4: {
        "name": "Floor 4 - Robotics Lab",
        "description": "Alan's command center - where good robots are built",
        "theme": "good",
        "color": CYAN,
        "ambient_color": (0, 100, 150)
    },
    5: {
        "name": "Floor 5 - Gym/Movement",
        "description": "Under construction - future fitness center",
        "theme": "neutral",
        "color": ORANGE,
        "ambient_color": (200, 150, 100)
    },
    6: {
        "name": "Floor 6 - Arts & Music",
        "description": "Creative space for artists and musicians",
        "theme": "neutral",
        "color": PURPLE,
        "ambient_color": (150, 50, 150)
    },
    7: {
        "name": "Floor 7 - Maker Space",
        "description": "Workshop for building and prototyping",
        "theme": "neutral",
        "color": (150, 100, 50),
        "ambient_color": (170, 120, 70)
    },
    8: {
        "name": "Floor 8 - Biotech Labs",
        "description": "Life sciences and biotech research",
        "theme": "neutral",
        "color": GREEN,
        "ambient_color": (50, 150, 50)
    },
    9: {
        "name": "Floor 9 - AI & Autonomous Systems",
        "description": "Advanced AI research and development",
        "theme": "neutral",
        "color": (100, 100, 200),
        "ambient_color": (120, 120, 220)
    },
    10: {
        "name": "Floor 10 - VCs & Accelerator",
        "description": "Venture capital and startup accelerator",
        "theme": "neutral",
        "color": GOLD,
        "ambient_color": (255, 200, 0)
    },
    11: {
        "name": "Floor 11 - Health & Longevity",
        "description": "Wellness and life extension research",
        "theme": "neutral",
        "color": (150, 255, 150),
        "ambient_color": (100, 200, 100)
    },
    12: {
        "name": "Floor 12 - Crypto/DeFi",
        "description": "Blockchain and decentralized finance",
        "theme": "neutral",
        "color": ORANGE,
        "ambient_color": (255, 140, 0)
    },
    14: {
        "name": "Floor 14 - Human Flourishing",
        "description": "No 13th floor! Philosophy and human potential",
        "theme": "neutral",
        "color": (255, 200, 255),
        "ambient_color": (255, 180, 255)
    },
    15: {
        "name": "Floor 15 - Coworking & Library",
        "description": "Shared workspace and knowledge repository",
        "theme": "neutral",
        "color": (180, 180, 200),
        "ambient_color": (200, 200, 220)
    },
    16: {
        "name": "Floor 16 - d/acc Lounge",
        "description": "Decentralized acceleration community space",
        "theme": "neutral",
        "color": MAGENTA,
        "ambient_color": (200, 0, 200)
    },
    17: {
        "name": "Roof - Secret Rave",
        "description": "Hidden party venue with city views",
        "theme": "party",
        "color": (255, 0, 255),
        "ambient_color": (255, 100, 255)
    }
}

# Elevator settings
ELEVATOR_WIDTH = 80
ELEVATOR_HEIGHT = 100
ELEVATOR_SPEED = 200  # Pixels per second
ELEVATOR_ACCELERATION = 100  # Pixels per second squared
ELEVATOR_MAX_CAPACITY = 6
ELEVATOR_DOOR_SPEED = 50  # Pixels per second

# Shaft settings
SHAFT_WIDTH = 120
SHAFT_X = SCREEN_WIDTH // 2 - SHAFT_WIDTH // 2
FLOOR_HEIGHT = 120
FLOOR_SPACING = 10

# NPC settings
NPC_WIDTH = 30
NPC_HEIGHT = 40
NPC_SPEED = 50  # Pixels per second
NPC_SPAWN_RATE = 3.0  # Seconds between spawns

# Special NPC settings
JOHN_SPAWN_DELAY = 5.0  # John appears after 5 seconds
ALAN_SPAWN_DELAY = 10.0  # Alan appears after 10 seconds
BAD_ROBOT_ESCAPE_RATE = 0.1  # Chance per second of bad robot escaping

# Game states
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"

# Player controls (for 2-player arcade)
PLAYER1_CONTROLS = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "action": pygame.K_SPACE,
    "open_doors": pygame.K_e
}

PLAYER2_CONTROLS = {
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "action": pygame.K_RETURN,
    "open_doors": pygame.K_RSHIFT
}

# Arcade cabinet buttons (mapped to keyboard for development)
ARCADE_BUTTON_1 = pygame.K_SPACE
ARCADE_BUTTON_2 = pygame.K_LSHIFT
ARCADE_BUTTON_3 = pygame.K_LCTRL
ARCADE_BUTTON_4 = pygame.K_LALT

# Font settings
FONT_NAME = "Arial"
FONT_SIZE_SMALL = 16
FONT_SIZE_MEDIUM = 24
FONT_SIZE_LARGE = 48
FONT_SIZE_TITLE = 72

# Sound settings
SOUND_ENABLED = True
MUSIC_VOLUME = 0.7
SFX_VOLUME = 0.8
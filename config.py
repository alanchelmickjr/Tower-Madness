"""
Configuration for Tower Madness / Elevator Operator
Arcade cabinet and game settings
"""

import pygame

# Arcade Cabinet Configuration
ARCADE_MODE = True  # Set to True for arcade cabinet deployment
FULLSCREEN = False  # Set to True for fullscreen mode at events
SHOW_CURSOR = True  # Hide cursor in arcade mode

# Display Configuration
DISPLAY_MODES = {
    "development": (1024, 768),
    "arcade_standard": (1280, 1024),
    "arcade_wide": (1920, 1080),
    "sf_tech_week": (1920, 1080)  # For Algorave projection
}

CURRENT_DISPLAY_MODE = "development"

# Player Configuration
DEFAULT_PLAYERS = 1
MAX_PLAYERS = 2
ENABLE_AI_PLAYERS = False  # Future feature for AI-controlled second player

# Control Schemes
CONTROL_SCHEMES = {
    "keyboard": {
        "player1": {
            "up": pygame.K_w,
            "down": pygame.K_s,
            "left": pygame.K_a,
            "right": pygame.K_d,
            "action": pygame.K_SPACE,
            "special": pygame.K_e
        },
        "player2": {
            "up": pygame.K_UP,
            "down": pygame.K_DOWN,
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "action": pygame.K_RETURN,
            "special": pygame.K_RSHIFT
        }
    },
    "arcade": {
        "player1": {
            "up": pygame.K_w,  # Mapped to joystick up
            "down": pygame.K_s,  # Mapped to joystick down
            "left": pygame.K_a,  # Mapped to joystick left
            "right": pygame.K_d,  # Mapped to joystick right
            "button1": pygame.K_SPACE,  # Red button
            "button2": pygame.K_LSHIFT,  # Blue button
            "button3": pygame.K_LCTRL,  # Yellow button
            "button4": pygame.K_LALT,  # Green button
        },
        "player2": {
            "up": pygame.K_UP,
            "down": pygame.K_DOWN,
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "button1": pygame.K_RETURN,
            "button2": pygame.K_RSHIFT,
            "button3": pygame.K_RCTRL,
            "button4": pygame.K_RALT,
        }
    }
}

# Audio Configuration
MASTER_VOLUME = 0.8
MUSIC_VOLUME = 0.7
SFX_VOLUME = 0.9
ENABLE_MUSIC = True
ENABLE_SFX = True

# Algorave specific settings
ALGORAVE_MODE = False  # Special effects for Algorave
BEAT_SYNC = False  # Sync game events to music beat
VISUAL_EFFECTS_LEVEL = "high"  # "low", "medium", "high", "ultra"

# Game Modes
GAME_MODES = {
    "elevator_operator": {
        "name": "Elevator Operator",
        "description": "Operate the elevator between good and evil",
        "enabled": True,
        "default": True
    },
    "robot_fighter": {
        "name": "Robot Fighter",
        "description": "Battle in the basement fight club",
        "enabled": False,  # Coming soon
        "default": False
    },
    "tower_climber": {
        "name": "Tower Climber",
        "description": "16 floor side-to-side climber",
        "enabled": False,  # Coming soon
        "default": False
    }
}

# Narrative Configuration
NARRATIVE_THEMES = {
    "classic": {
        "good_floor": 4,
        "evil_floor": -1,
        "escape_floor": 5,
        "good_name": "Good Robot Lab",
        "evil_name": "Robot Fight Club",
        "escape_name": "Roof Rave"
    },
    "cyberpunk": {
        "good_floor": 4,
        "evil_floor": -1,
        "escape_floor": 5,
        "good_name": "AI Liberation Front",
        "evil_name": "Corporate Control Center",
        "escape_name": "Sky Freedom"
    }
}

CURRENT_NARRATIVE = "classic"

# Difficulty Settings
DIFFICULTY_LEVELS = {
    "easy": {
        "npc_spawn_rate": 4.0,
        "npc_patience": 30.0,
        "elevator_speed": 250,
        "score_multiplier": 0.8
    },
    "normal": {
        "npc_spawn_rate": 3.0,
        "npc_patience": 20.0,
        "elevator_speed": 200,
        "score_multiplier": 1.0
    },
    "hard": {
        "npc_spawn_rate": 2.0,
        "npc_patience": 15.0,
        "elevator_speed": 150,
        "score_multiplier": 1.5
    },
    "chaos": {
        "npc_spawn_rate": 1.0,
        "npc_patience": 10.0,
        "elevator_speed": 300,
        "score_multiplier": 2.0
    }
}

CURRENT_DIFFICULTY = "normal"

# Special Characters
SPECIAL_CHARACTERS = {
    "john_the_doorman": {
        "enabled": True,
        "spawn_chance": 0.1,
        "patience": 999,
        "score_bonus": 50,
        "color": (50, 50, 150),
        "description": "The doorman who connects everyone"
    },
    "ai_overseer": {
        "enabled": False,  # Future feature
        "spawn_chance": 0.05,
        "patience": 60,
        "score_bonus": 100,
        "color": (255, 255, 255),
        "description": "The mysterious AI watching everything"
    }
}

# Performance Settings
TARGET_FPS = 60
VSYNC = True
HARDWARE_ACCELERATION = True

# Debug Settings
DEBUG_MODE = False
SHOW_FPS = False
SHOW_HITBOXES = False
INVINCIBLE_MODE = False

# Leaderboard Configuration
ENABLE_LEADERBOARD = True
LEADERBOARD_SIZE = 10
LEADERBOARD_FILE = "highscores.json"

# Network Configuration (for future online features)
ENABLE_NETWORK = False
SERVER_URL = "https://towermadness.game"
API_VERSION = "v1"

def get_display_size():
    """Get the current display size based on mode."""
    return DISPLAY_MODES.get(CURRENT_DISPLAY_MODE, DISPLAY_MODES["development"])

def get_control_scheme(player_num=1):
    """Get control scheme for a player."""
    scheme = "arcade" if ARCADE_MODE else "keyboard"
    player_key = f"player{player_num}"
    return CONTROL_SCHEMES[scheme].get(player_key, CONTROL_SCHEMES["keyboard"]["player1"])

def get_difficulty_settings():
    """Get current difficulty settings."""
    return DIFFICULTY_LEVELS.get(CURRENT_DIFFICULTY, DIFFICULTY_LEVELS["normal"])

def get_narrative_theme():
    """Get current narrative theme."""
    return NARRATIVE_THEMES.get(CURRENT_NARRATIVE, NARRATIVE_THEMES["classic"])

# Initialize Pygame mixer with config
def init_audio():
    """Initialize audio system with configured settings."""
    pygame.mixer.init(
        frequency=44100,
        size=-16,
        channels=2,
        buffer=512
    )
    pygame.mixer.music.set_volume(MUSIC_VOLUME * MASTER_VOLUME)
    
# Event-specific configurations
SF_TECH_WEEK_CONFIG = {
    "event_mode": True,
    "attract_mode": True,  # Demo mode when no one is playing
    "attract_timeout": 30,  # Seconds before returning to attract mode
    "show_qr_code": True,  # Show QR code for more info
    "social_features": True,  # Enable social media integration
    "party_mode": True,  # Extra visual effects for the rave
}
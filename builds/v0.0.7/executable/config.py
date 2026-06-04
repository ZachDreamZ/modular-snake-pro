VERSION = "0.0.7"

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
BLOCK_SIZE = 20
BASE_FPS = 10

# States
STATE_TITLE = "TITLE"
STATE_MODE_SELECT = "MODE_SELECT"
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"
STATE_GAMEOVER = "GAMEOVER"
STATE_COUNTDOWN = "COUNTDOWN"

# Game Modes
MODE_CLASSIC = "CLASSIC"
MODE_TIME_RUSH = "TIME_RUSH"
MODE_MAZE_HELL = "MAZE_HELL"

GAME_MODES = {
    MODE_CLASSIC: {
        "name": "Classic",
        "base_speed": 10,
        "timer": None,
        "start_stage": 1,
        "boss_enabled": True
    },
    MODE_TIME_RUSH: {
        "name": "Time Rush",
        "base_speed": 15,
        "timer": 60,
        "start_stage": 1,
        "boss_enabled": False
    },
    MODE_MAZE_HELL: {
        "name": "Maze Hell",
        "base_speed": 10,
        "timer": None,
        "start_stage": 4,
        "boss_enabled": True
    }
}

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_DARK_GREEN = (0, 100, 0)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)  # Golden Food
COLOR_PURPLE = (128, 0, 128)  # Poison Food
COLOR_GREY = (128, 128, 128)  # Obstacles
COLOR_BLUE = (0, 0, 255)      # AI Snake
COLOR_GOLD = (255, 215, 0)    # Gold
COLOR_DARK_BLUE = (0, 0, 150) # AI Snake Dark

# Accessibility: Colorblind Palettes
COLORBLIND_PALETTES = {
    "none": {
        "green": (0, 255, 0),
        "red": (255, 0, 0),
        "yellow": (255, 255, 0),
        "purple": (128, 0, 128),
        "blue": (0, 0, 255),
    },
    "protanopia": {
        "green": (180, 180, 0),
        "red": (150, 100, 0),
        "yellow": (255, 255, 0),
        "purple": (100, 100, 180),
        "blue": (0, 0, 255),
    },
    "deuteranopia": {
        "green": (180, 180, 0),
        "red": (200, 100, 0),
        "yellow": (255, 255, 0),
        "purple": (120, 120, 180),
        "blue": (0, 0, 255),
    },
    "tritanopia": {
        "green": (0, 255, 0),
        "red": (255, 0, 0),
        "yellow": (255, 100, 100),
        "purple": (128, 0, 128),
        "blue": (0, 255, 255),
    }
}
COLOR_BOSS_RED = (220, 20, 60)
COLOR_BOSS_GOLD = (255, 215, 0)
COLOR_PLASMA_BLUE = (0, 255, 255)

# Rarity Colors
COLOR_RARITY_COMMON = (169, 169, 169)
COLOR_RARITY_EPIC = (160, 32, 240)
COLOR_RARITY_LEGENDARY = (255, 215, 0)

# Checkered Board Colors
COLOR_SLATE_GRAY = (112, 128, 144)
COLOR_FOREST_GREEN = (34, 60, 34)

# Themes
THEMES = {
    "default": {
        "name": "Classic Arcade",
        "bg_color": (0, 0, 0),
        "snake_color": (0, 255, 0),
        "snake_color_dark": (0, 100, 0),
        "food_normal": (255, 0, 0),
        "food_golden": (255, 255, 0),
        "food_poison": (128, 0, 128),
        "required_achievement": None,
        "rarity": "common"
    },
    "neon": {
        "name": "Cyberpunk Neon",
        "bg_color": (0, 0, 0),
        "snake_color": (255, 0, 255),
        "snake_color_dark": (128, 0, 128),
        "food_normal": (0, 255, 255),
        "food_golden": (255, 255, 0),
        "food_poison": (128, 0, 128),
        "required_achievement": None,
        "rarity": "epic"
    },
    "dark": {
        "name": "Retro GameBoy",
        "bg_color": (155, 188, 15),
        "snake_color": (15, 56, 15),
        "snake_color_dark": (0, 0, 0),
        "food_normal": (48, 98, 48),
        "food_golden": (15, 56, 15),
        "food_poison": (15, 56, 15),
        "required_achievement": None,
        "rarity": "common"
    },
    "golden_mecha": {
        "name": "Golden Mecha",
        "bg_color": (20, 20, 20),
        "snake_color": (255, 215, 0),
        "snake_color_dark": (184, 134, 11),
        "food_normal": (255, 255, 255),
        "food_golden": (255, 255, 0),
        "food_poison": (128, 0, 128),
        "required_achievement": "Dragon Slayer",
        "rarity": "legendary"
    },
    "ghost": {
        "name": "Ghost",
        "bg_color": (10, 10, 30),
        "snake_color": (200, 200, 255),
        "snake_color_dark": (100, 100, 150),
        "food_normal": (100, 255, 100),
        "food_golden": (255, 255, 0),
        "food_poison": (128, 0, 128),
        "required_achievement": "Speed Demon",
        "rarity": "legendary"
    },
    "void": {
        "name": "The Void",
        "bg_color": (15, 0, 25),
        "snake_color": (180, 0, 255),
        "snake_color_dark": (40, 0, 60),
        "food_normal": (0, 255, 255),
        "food_golden": (255, 255, 0),
        "food_poison": (255, 0, 255),
        "required_achievement": "Void Walker",
        "rarity": "legendary"
    }
}

# Typography
FONT_SIZE_HUGE = 48
FONT_SIZE_MEDIUM = 24
FONT_SIZE_SMALL = 14
FONT_SIZE_TINY = 12

# Food Types
FOOD_NORMAL = "normal"
FOOD_GOLDEN = "golden"
FOOD_POISON = "poison"
FOOD_GHOST = "ghost"
FOOD_SHIELD = "shield"
FOOD_MISSILE = "missile"

# Achievement definitions
ACHIEVEMENT_DEFS = {
    "First Blood": {
        "name": "First Blood",
        "description": "Score your first 10 points",
        "condition": "score >= 10",
        "icon": "🏆"
    },
    "Marathon": {
        "name": "Marathon",
        "description": "Reach a score of 500",
        "condition": "score >= 500",
        "icon": "🏃"
    },
    "Dragon Slayer": {
        "name": "Dragon Slayer",
        "description": "Defeat the boss and achieve victory",
        "condition": "boss_victory",
        "icon": "🐉"
    },
    "Speed Demon": {
        "name": "Speed Demon",
        "description": "Survive 120 seconds in Time Rush mode",
        "condition": "time_rush_survival >= 120",
        "icon": "⚡"
    },
    "Void Walker": {
        "name": "Void Walker",
        "description": "Survive 120 seconds in Maze Hell mode",
        "condition": "maze_survival >= 120",
        "icon": "🌀"
    },
    "Combo Master": {
        "name": "Combo Master",
        "description": "Reach a 10x combo",
        "condition": "combo >= 10",
        "icon": "💥"
    },
    "Point Collector": {
        "name": "Point Collector",
        "description": "Collect 1000 total points across all sessions",
        "condition": "total_points >= 1000",
        "icon": "⭐"
    },
    "Unstoppable": {
        "name": "Unstoppable",
        "description": "Win 3 boss battles",
        "condition": "boss_wins >= 3",
        "icon": "🛡️"
    }
}

# Objective definitions for play
OBJECTIVE_DEFS = {
    "score_100": {
        "name": "Century",
        "description": "Score 100 points in a single game",
        "condition": "score >= 100",
        "reward": 50
    },
    "score_250": {
        "name": "Quarter Millennium",
        "description": "Score 250 points in a single game",
        "condition": "score >= 250",
        "reward": 100
    },
    "eat_50_food": {
        "name": "Hungry Snake",
        "description": "Eat 50 food items total",
        "condition": "total_food_eaten >= 50",
        "reward": 75
    },
    "survive_3_min": {
        "name": "Survivor",
        "description": "Survive 3 minutes in any mode",
        "condition": "survival_time >= 180",
        "reward": 100
    },
    "combo_5": {
        "name": "Chain Reaction",
        "description": "Reach a 5x combo",
        "condition": "combo_reached >= 5",
        "reward": 30
    }
}

# Balancing parameters
FOOD_SCORES = {
    "normal": 10,
    "golden": 15,
    "poison": -20,
    "shield": 0,
    "missile": 20,
    "ghost": 10
}

COMBO_MULTIPLIER_STEP = 5  # Every 5 combo gives +0.2x
COMBO_MAX_MULTIPLIER = 2.0
FRENZY_COMBO_THRESHOLD = 10
GHOST_TIMER_DURATION = 300
FRENZY_TIMER_DURATION = 300
SHIELD_TIMER_UNIT = 10  # Multiplied by game_speed

# Spawn weights for food types (higher = more common)
FOOD_SPAWN_WEIGHTS = {
    "normal": 50,
    "golden": 20,
    "poison": 10,
    "shield": 8,
    "missile": 7,
    "ghost": 5
}

# v0.0.7 New Features
CONTEXTUAL_HINTS = {
    "first_game": [
        ("Use arrow keys or WASD to move", 180),
        ("Eat red food to grow and score points", 360),
        ("Avoid purple poison food and walls!", 540),
    ],
    "combo_tip": [
        ("Chain food eats for combo multiplier!", 120),
        ("Combo resets if you wait too long", 300),
    ],
    "time_rush_intro": [
        ("Race against the clock! Time Rush mode", 180),
        ("Eat food to extend your timer", 360),
    ],
    "maze_hell_intro": [
        ("Navigating complex mazes in Maze Hell", 180),
        ("Survive. Conquer. Escape.", 360),
    ],
    "boss_intro": [
        ("BOSS ENCOUNTER! Fire missiles with food!", 120),
        ("Watch out for boss hazards on the field", 300),
    ]
}
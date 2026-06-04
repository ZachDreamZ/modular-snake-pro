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
COLOR_DARK_BLUE = (0, 0, 150) # AI Snake Dark
COLOR_BOSS_RED = (220, 20, 60) # Crimson for Boss
COLOR_BOSS_GOLD = (255, 215, 0) # Gold for Boss
COLOR_PLASMA_BLUE = (0, 255, 255) # Projectile color

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
        "snake_color": (255, 0, 255), # Neon Pink
        "snake_color_dark": (128, 0, 128),
        "food_normal": (0, 255, 255), # Neon Cyan
        "food_golden": (255, 255, 0),
        "food_poison": (128, 0, 128),
        "required_achievement": None,
        "rarity": "epic"
    },
    "dark": {
        "name": "Retro GameBoy",
        "bg_color": (155, 188, 15), # Light greenish-grey
        "snake_color": (15, 56, 15), # Dark olive
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
        "snake_color": (255, 215, 0), # Gold
        "snake_color_dark": (184, 134, 11), # Dark Gold
        "food_normal": (255, 255, 255),
        "food_golden": (255, 255, 0),
        "food_poison": (128, 0, 128),
        "required_achievement": "Dragon Slayer",
        "rarity": "legendary"
    },
    "ghost": {
        "name": "Ghost",
        "bg_color": (10, 10, 30),
        "snake_color": (200, 200, 255), # Pale blue
        "snake_color_dark": (100, 100, 150),
        "food_normal": (100, 255, 100),
        "food_golden": (255, 255, 0),
        "food_poison": (128, 0, 128),
        "required_achievement": "Speed Demon",
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
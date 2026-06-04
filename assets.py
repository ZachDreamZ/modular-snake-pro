import json
import os
import pygame
import urllib.request

SAVE_FILE = "total_points.json"
LEADERBOARD_FILE = "leaderboard.json"
ACHIEVEMENTS_FILE = "achievements.json"
SETTINGS_FILE = "settings.json"

def download_assets():
    """Automatically downloads required game assets from the web."""
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    # Asset mapping: filename -> URL (using Oran Berry as a reliable red fruit sprite)
    assets_to_download = {
        "apple.png": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/oran-berry.png"
    }
    
    for filename, url in assets_to_download.items():
        path = os.path.join(assets_dir, filename)
        if not os.path.exists(path):
            try:
                print(f"Downloading {filename}...")
                urllib.request.urlretrieve(url, path)
                print(f"Successfully downloaded {filename}")
            except Exception as e:
                print(f"Failed to download {filename}: {e}")

# Sound Paths
SOUND_EAT = "assets/sounds/eat.wav"
SOUND_POWERUP = "assets/sounds/powerup.wav"
SOUND_CRASH = "assets/sounds/crash.wav"
SOUND_VICTORY = "assets/sounds/victory.wav"
SOUND_CLICK = "assets/sounds/click.wav"

class SoundManager:
    _instance = None
    music_enabled = True
    sfx_enabled = True

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SoundManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        try:
            pygame.mixer.init()
            self.sounds = {}
            self._load_sound("eat", SOUND_EAT)
            self._load_sound("powerup", SOUND_POWERUP)
            self._load_sound("crash", SOUND_CRASH)
            self._load_sound("victory", SOUND_VICTORY)
            self._load_sound("click", SOUND_CLICK)
        except pygame.error as e:
            print(f"Warning: Pygame mixer could not be initialized: {e}")
            self.sounds = {}
        
        self._initialized = True

    def _load_sound(self, name, path):
        try:
            self.sounds[name] = pygame.mixer.Sound(path)
        except (pygame.error, FileNotFoundError) as e:
            print(f"Warning: Could not load sound {path}: {e}")
            self.sounds[name] = None

    def play(self, name):
        if not self.sfx_enabled:
            return
        sound = self.sounds.get(name)
        if sound:
            sound.play()

    def set_music(self, enabled):
        self.music_enabled = enabled
        # In a real game, we'd call pygame.mixer.music.pause()/unpause()
        print(f"Music {'enabled' if enabled else 'disabled'}")

    def set_sfx(self, enabled):
        self.sfx_enabled = enabled
        print(f"SFX {'enabled' if enabled else 'disabled'}")

# Global instance
sound_manager = SoundManager()

def _read_data():
    """Helper to read the persistence data file."""
    if not os.path.exists(SAVE_FILE):
        return {}
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def _write_data(data):
    """Helper to write the persistence data file."""
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
    except IOError as e:
        print(f"Error saving data: {e}")

def load_high_score():
    """Loads the high score from the JSON file."""
    return _read_data().get("high_score", 0)

def save_high_score(score):
    """Saves the high score to the JSON file if it's higher than the current one."""
    data = _read_data()
    if score > data.get("high_score", 0):
        data["high_score"] = score
        _write_data(data)

def load_total_points():
    """Loads the total collected points from the JSON file."""
    return _read_data().get("points", 0)

def save_total_points(points):
    """Saves the total accumulated points to the JSON file."""
    data = _read_data()
    data["points"] = points
    _write_data(data)

def update_total_points(delta):
    """Increments total points by a specific amount (e.g., points from a game)."""
    current_total = load_total_points()
    new_total = current_total + delta
    save_total_points(new_total)
    return new_total

def update_score(score):
    """Updates both high score and total points based on the final game score."""
    save_high_score(score)
    update_total_points(score)

def load_unlocked_themes():
    """Loads the list of unlocked themes from the JSON file."""
    data = _read_data()
    return data.get("unlocked_themes", ["default"])

def save_unlocked_themes(themes):
    """Saves the list of unlocked themes to the JSON file."""
    data = _read_data()
    data["unlocked_themes"] = themes
    _write_data(data)

def load_leaderboard():
    """Loads the top 5 high scores."""
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def load_achievements():
    """Loads the list of earned achievements."""
    if not os.path.exists(ACHIEVEMENTS_FILE):
        return []
    try:
        with open(ACHIEVEMENTS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_achievements(achievements):
    """Saves the list of earned achievements."""
    try:
        with open(ACHIEVEMENTS_FILE, "w") as f:
            json.dump(achievements, f)
    except IOError as e:
        print(f"Error saving achievements: {e}")

def save_leaderboard(leaderboard):
    """Saves the top 5 high scores."""
    try:
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(leaderboard[:5], f)
    except IOError as e:
        print(f"Error saving leaderboard: {e}")

def check_high_score(score):
    """Returns True if the score qualifies for the top 5."""
    leaderboard = load_leaderboard()
    if len(leaderboard) < 5:
        return True
    return score > min(entry["score"] for entry in leaderboard)

def load_settings():
    """Loads game settings from settings.json."""
    if not os.path.exists(SETTINGS_FILE):
        return {"music": True, "sfx": True}
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"music": True, "sfx": True}

def save_settings(settings):
    """Saves game settings to settings.json."""
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f)
    except IOError as e:
        print(f"Error saving settings: {e}")

import json
import os
import shutil
import pygame
from pathlib import Path

# Persistence files
SAVE_FILE = "total_points.json"
LEADERBOARD_FILE = "leaderboard.json"
ACHIEVEMENTS_FILE = "achievements.json"
SETTINGS_FILE = "settings.json"

# Organized asset folders
ASSET_ROOT = Path("assets")
ASSET_DIRS = {
    "sfx": ASSET_ROOT / "sfx",
    "bgm": ASSET_ROOT / "bgm",
    "images": ASSET_ROOT / "images",
    "screenshots": ASSET_ROOT / "screenshots",
    "fonts": ASSET_ROOT / "fonts",
    "raw": ASSET_ROOT
}

# Default filenames (logical names -> relative paths)
SOUND_EAT = str(ASSET_DIRS["sfx"] / "eat.wav")
SOUND_POWERUP = str(ASSET_DIRS["sfx"] / "powerup.wav")
SOUND_CRASH = str(ASSET_DIRS["sfx"] / "crash.wav")
SOUND_VICTORY = str(ASSET_DIRS["sfx"] / "victory.wav")
SOUND_CLICK = str(ASSET_DIRS["sfx"] / "click.wav")

BGM_MAIN_MP3 = str(ASSET_DIRS["bgm"] / "bgm_main.mp3")
IMAGE_APPLE = str(ASSET_DIRS["images"] / "apple.png")

# Ensure folders exist and attempt to reorganize legacy files into the new structure.
def _ensure_asset_structure_and_migrate():
    ASSET_ROOT.mkdir(exist_ok=True)
    for d in ASSET_DIRS.values():
        d.mkdir(parents=True, exist_ok=True)

    # Move top-level known files into new subfolders if they exist
    # images
    legacy_images = ["apple.png"]
    for img in legacy_images:
        src = ASSET_ROOT / img
        dst = ASSET_DIRS["images"] / img
        if src.exists() and not dst.exists():
            try:
                shutil.move(str(src), str(dst))
            except Exception:
                pass

    # bgm (common name patterns)
    for pattern in ["bgm_main.mp3", "bgm_main.ogg", "bgm_main.wav"]:
        src = ASSET_ROOT / pattern
        dst = ASSET_DIRS["bgm"] / pattern
        if src.exists() and not dst.exists():
            try:
                shutil.move(str(src), str(dst))
            except Exception:
                pass

    # If there's an old 'sounds' directory, move its files to sfx
    old_sounds_dir = ASSET_ROOT / "sounds"
    if old_sounds_dir.exists() and old_sounds_dir.is_dir():
        for file in old_sounds_dir.iterdir():
            if file.is_file():
                try:
                    shutil.move(str(file), str(ASSET_DIRS["sfx"] / file.name))
                except Exception:
                    pass
        try:
            old_sounds_dir.rmdir()
        except Exception:
            pass

    # If fonts folder already exists at root, move inside fonts dir
    legacy_fonts = ASSET_ROOT / "fonts"
    if legacy_fonts.exists() and legacy_fonts.is_dir():
        # already in place -> ensure moved under ASSET_DIRS fonts
        for f in legacy_fonts.iterdir():
            if f.is_file():
                target = ASSET_DIRS["fonts"] / f.name
                if not target.exists():
                    try:
                        shutil.move(str(f), str(target))
                    except Exception:
                        pass

# Call migration at import time (safe, idempotent)
_ensure_asset_structure_and_migrate()

# AssetManager: loads images/sounds/fonts once and caches them.
class AssetManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssetManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        # Lazy init pygame components only when available
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self._initialized = True

    # Image loader returns a pygame.Surface cached.
    # On failure it will try reasonable fallback paths and return a lightweight
    # placeholder Surface instead of None to avoid runtime crashes in UI.
    def load_image(self, name, path, convert_alpha=True):
        if name in self.images:
            return self.images[name]

        # Normalize input to Path
        try:
            p = Path(path)
        except Exception:
            p = None

        candidates = []
        if p:
            candidates.append(p)
        # try by logical name inside images dir
        try:
            candidates.append(ASSET_DIRS["images"] / name)
            candidates.append(ASSET_DIRS["images"] / f"{name}.png")
        except Exception:
            pass

        for cand in candidates:
            try:
                if cand and Path(cand).exists():
                    img = pygame.image.load(str(cand))
                    if convert_alpha:
                        img = img.convert_alpha()
                    else:
                        img = img.convert()
                    self.images[name] = img
                    return img
            except Exception:
                # try next candidate
                pass

        # Final fallback: generate a simple placeholder Surface so callers can still blit.
        placeholder = None
        try:
            # create a small rounded-rect style placeholder
            placeholder = pygame.Surface((64, 64), pygame.SRCALPHA)
            placeholder.fill((40, 40, 40, 255))
            try:
                pygame.draw.rect(placeholder, (80, 80, 80), pygame.Rect(4, 4, 56, 56), border_radius=8)
            except Exception:
                # pygame.draw may not support border_radius on some builds; fall back to rect
                pygame.draw.rect(placeholder, (80, 80, 80), pygame.Rect(4, 4, 56, 56))
        except Exception:
            placeholder = None

        self.images[name] = placeholder
        return placeholder

    # Sound loader returns a pygame.mixer.Sound cached
    def load_sound(self, name, path):
        if name in self.sounds:
            return self.sounds[name]
        try:
            snd = pygame.mixer.Sound(str(path))
            self.sounds[name] = snd
            return snd
        except Exception:
            self.sounds[name] = None
            return None

    # Font loader returns a pygame.font.Font cached
    def load_font(self, name, path_or_size, size=None):
        # path_or_size can be either a path (with size provided) or a system font name (string) when size provided
        key = f"{name}_{size or path_or_size}"
        if key in self.fonts:
            return self.fonts[key]
        try:
            if isinstance(path_or_size, (int, float)) and size is None:
                # system font by size only
                font = pygame.font.SysFont(None, int(path_or_size))
            elif size is None:
                # path_or_size is size
                font = pygame.font.SysFont(None, int(path_or_size))
            else:
                # path provided
                font = pygame.font.Font(str(path_or_size), int(size))
            self.fonts[key] = font
            return font
        except Exception:
            self.fonts[key] = None
            return None

# Backwards-compatible SoundManager wrapper that uses AssetManager caching
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
        except Exception:
            # if mixer cannot init, continue with silent fallback
            pass
        self._assets = AssetManager()
        # Preload known sounds (if files exist)
        self._preload_sound("eat", SOUND_EAT)
        self._preload_sound("powerup", SOUND_POWERUP)
        self._preload_sound("crash", SOUND_CRASH)
        self._preload_sound("victory", SOUND_VICTORY)
        self._preload_sound("click", SOUND_CLICK)
        self._initialized = True

    def _preload_sound(self, name, path):
        p = Path(path)
        if p.exists():
            self._assets.load_sound(name, p)

    def play(self, name):
        if not self.sfx_enabled:
            return
        snd = self._assets.sounds.get(name)
        if snd:
            try:
                snd.play()
            except Exception:
                pass

    def set_music(self, enabled):
        self.music_enabled = enabled
        try:
            pygame.mixer.music.set_volume(1.0 if enabled else 0.0)
        except Exception:
            pass

    def play_music(self, filename, loop=-1):
        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play(loop)
            pygame.mixer.music.set_volume(1.0 if self.music_enabled else 0.0)
        except Exception:
            pass

    def stop_music(self):
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

    def fade_music(self, duration=1000):
        try:
            pygame.mixer.music.fadeout(duration)
        except Exception:
            pass

    def set_sfx(self, enabled):
        self.sfx_enabled = enabled

# Global instances
asset_manager = AssetManager()
sound_manager = SoundManager()

# Legacy helper functions for persistence and leaderboard (kept intact)
def _read_data():
    if not os.path.exists(SAVE_FILE):
        return {}
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def _write_data(data):
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
    except IOError:
        pass

def load_high_score():
    return _read_data().get("high_score", 0)

def save_high_score(score):
    data = _read_data()
    if score > data.get("high_score", 0):
        data["high_score"] = score
        _write_data(data)

def load_total_points():
    return _read_data().get("points", 0)

def save_total_points(points):
    data = _read_data()
    data["points"] = points
    _write_data(data)

def update_total_points(delta):
    current_total = load_total_points()
    new_total = current_total + delta
    save_total_points(new_total)
    return new_total

def update_score(score):
    save_high_score(score)
    update_total_points(score)

def load_unlocked_themes():
    data = _read_data()
    return data.get("unlocked_themes", ["default"])

def save_unlocked_themes(themes):
    data = _read_data()
    data["unlocked_themes"] = themes
    _write_data(data)

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def load_achievements():
    if not os.path.exists(ACHIEVEMENTS_FILE):
        return []
    try:
        with open(ACHIEVEMENTS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_achievements(achievements):
    try:
        with open(ACHIEVEMENTS_FILE, "w") as f:
            json.dump(achievements, f)
    except IOError:
        pass

def save_leaderboard(leaderboard):
    try:
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(leaderboard[:5], f)
    except IOError:
        pass

def check_high_score(score):
    leaderboard = load_leaderboard()
    if len(leaderboard) < 5:
        return True
    return score > min(entry["score"] for entry in leaderboard)

def load_settings():
    defaults = {"music": True, "sfx": True}
    if not os.path.exists(SETTINGS_FILE):
        return defaults
    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
            return {**defaults, **settings}
    except (json.JSONDecodeError, IOError):
        return defaults

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f)
    except IOError:
        pass
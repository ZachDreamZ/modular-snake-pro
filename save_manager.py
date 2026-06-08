import json
import os

SAVE_FILE = "total_points.json"
LEADERBOARD_FILE = "leaderboard.json"
ACHIEVEMENTS_FILE = "achievements.json"
SETTINGS_FILE = "settings.json"
OBJECTIVES_FILE = "objectives_progress.json"
STATS_FILE = "stats.json"

def _read_save():
    if not os.path.exists(SAVE_FILE):
        return {}
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def _write_save(data):
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
    except IOError:
        pass

def save_high_score(score):
    data = _read_save()
    if score > data.get("high_score", 0):
        data["high_score"] = score
    _write_save(data)

def get_high_score():
    return _read_save().get("high_score", 0)

def save_total_points(points):
    data = _read_save()
    data["points"] = points
    _write_save(data)

def load_total_points():
    return _read_save().get("points", 0)

def load_unlocked_themes():
    return _read_save().get("unlocked_themes", ["default"])

def save_unlocked_themes(themes):
    data = _read_save()
    data["unlocked_themes"] = themes
    _write_save(data)

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_leaderboard(leaderboard):
    try:
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(leaderboard[:5], f)
    except IOError:
        pass

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

def check_high_score(score):
    leaderboard = load_leaderboard()
    if len(leaderboard) < 5:
        return True
    return score > min(entry["score"] for entry in leaderboard)

def load_settings():
    defaults = {"music": True, "sfx": True, "font_scale": 1.0, "colorblind": "none", "language": "en"}
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

def save_objectives_progress(progress):
    """Save objectives completion tracking data."""
    with open(OBJECTIVES_FILE, "w") as f:
        json.dump(progress, f)

def load_objectives_progress():
    """Load objectives completion tracking data."""
    if os.path.exists(OBJECTIVES_FILE):
        try:
            with open(OBJECTIVES_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {"completed": [], "total_food_eaten": 0, "total_games": 0, "total_time": 0, "max_combo": 0, "boss_wins": 0}
    return {"completed": [], "total_food_eaten": 0, "total_games": 0, "total_time": 0, "max_combo": 0, "boss_wins": 0}

def save_stats(stats):
    """Save persistent game stats."""
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)

def load_stats():
    """Load persistent game stats."""
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {"total_food_eaten": 0, "total_games": 0, "total_time": 0, "max_combo": 0, "boss_wins": 0, "total_score": 0, "games_played": 0}
    return {"total_food_eaten": 0, "total_games": 0, "total_time": 0, "max_combo": 0, "boss_wins": 0, "total_score": 0, "games_played": 0}

def update_total_points(delta):
    current_total = load_total_points()
    new_total = current_total + delta
    save_total_points(new_total)
    return new_total
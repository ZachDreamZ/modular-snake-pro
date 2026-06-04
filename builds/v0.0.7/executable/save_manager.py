import json
import os

HIGHSCORE_FILE = "highscore.json"
LEADERBOARD_FILE = "leaderboard.json"
TOTAL_POINTS_FILE = "total_points.json"
OBJECTIVES_FILE = "objectives_progress.json"
STATS_FILE = "stats.json"

def save_high_score(score):
    data = {}
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            data = {}
    old_high = data.get("high_score", 0)
    if score > old_high:
        data["high_score"] = score
    data["total_points"] = data.get("total_points", 0) + score
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump(data, f)

def get_high_score():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                data = json.load(f)
            return data.get("high_score", 0)
        except (json.JSONDecodeError, IOError):
            return 0
    return 0

def save_total_points(points):
    data = {}
    if os.path.exists(TOTAL_POINTS_FILE):
        try:
            with open(TOTAL_POINTS_FILE, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            data = {}
    data["points"] = points
    with open(TOTAL_POINTS_FILE, "w") as f:
        json.dump(data, f)

def load_total_points():
    if os.path.exists(TOTAL_POINTS_FILE):
        try:
            with open(TOTAL_POINTS_FILE, "r") as f:
                data = json.load(f)
            return data.get("points", 0)
        except (json.JSONDecodeError, IOError):
            return 0
    return 0

def get_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f)

def load_leaderboard():
    return get_leaderboard()

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
import json
import os
from datetime import datetime

class AnalyticsManager:
    def __init__(self, filename="analytics.json"):
        self.filename = filename
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading analytics: {e}")
        
        return {
            "sessions": 0,
            "total_games": 0,
            "total_score": 0,
            "deaths": {
                "wall": 0,
                "self": 0,
                "boss": 0,
                "timer": 0
            },
            "theme_usage": {},
            "last_played": None
        }

    def save_data(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"Error saving analytics: {e}")

    def log_session_start(self):
        self.data["sessions"] += 1
        self.data["last_played"] = datetime.now().isoformat()
        self.save_data()

    def log_game_end(self, score, cause):
        self.data["total_games"] += 1
        self.data["total_score"] += score
        if cause in self.data["deaths"]:
            self.data["deaths"][cause] += 1
        else:
            self.data["deaths"][cause] = self.data["deaths"].get(cause, 0) + 1
        self.save_data()

    def log_theme_equip(self, theme_id):
        self.data["theme_usage"][theme_id] = self.data["theme_usage"].get(theme_id, 0) + 1
        self.save_data()

# Singleton instance
analytics = AnalyticsManager()
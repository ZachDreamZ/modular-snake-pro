import json
import os

SAVE_FILE = "save_data.json"

def load_save_data():
    """Loads save data from the local JSON file."""
    if not os.path.exists(SAVE_FILE):
        return {"high_score": 0}
    
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"high_score": 0}

def save_high_score(score):
    """Saves the high score if the provided score is higher than the existing one."""
    data = load_save_data()
    if score > data.get("high_score", 0):
        data["high_score"] = score
        try:
            with open(SAVE_FILE, "w") as f:
                json.dump(data, f, indent=4)
            return True
        except IOError:
            return False
    return False

def get_high_score():
    """Returns the current high score."""
    return load_save_data().get("high_score", 0)
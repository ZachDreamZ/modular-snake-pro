import json
import os
from config import THEMES

class ModManager:
    def __init__(self, mods_dir="mods"):
        self.mods_dir = mods_dir
        self.loaded_mods = []
        self.load_mods()

    def load_mods(self):
        if not os.path.exists(self.mods_dir):
            os.makedirs(self.mods_dir)
            return

        for mod_folder in os.listdir(self.mods_dir):
            mod_path = os.path.join(self.mods_dir, mod_folder)
            if os.path.isdir(mod_path):
                config_path = os.path.join(mod_path, "mod.json")
                if os.path.exists(config_path):
                    try:
                        with open(config_path, "r", encoding="utf-8") as f:
                            mod_config = json.load(f)
                            self.apply_mod(mod_config)
                            self.loaded_mods.append(mod_config.get("name", mod_folder))
                    except Exception as e:
                        print(f"Error loading mod {mod_folder}: {e}")

    def apply_mod(self, config):
        # Handle theme overrides/additions
        overrides = config.get("overrides", {})
        themes = overrides.get("themes", {})
        for theme_id, theme_data in themes.items():
            # Ensure required fields are present
            required = ["name", "bg_color", "snake_color", "snake_color_dark", "food_normal", "food_golden", "food_poison"]
            if all(k in theme_data for k in required):
                # Add to global THEMES dictionary
                THEMES[theme_id] = theme_data
                print(f"Mod loaded theme: {theme_data['name']}")

    def get_loaded_mods(self):
        return self.loaded_mods

# Singleton instance
mod_manager = ModManager()
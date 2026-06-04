import json
import os
from config import VERSION

class LocalizationManager:
    def __init__(self, default_lang="en"):
        self.default_lang = default_lang
        self.current_lang = default_lang
        self.translations = {}
        self.load_translations(default_lang)

    def load_translations(self, lang):
        path = f"localization/{lang}.json"
        try:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    self.translations = json.load(f)
                self.current_lang = lang
            else:
                print(f"Localization file not found: {path}. Falling back to {self.default_lang}")
                if lang != self.default_lang:
                    self.load_translations(self.default_lang)
        except Exception as e:
            print(f"Error loading localization file {path}: {e}")
            if lang != self.default_lang:
                self.load_translations(self.default_lang)

    def set_language(self, lang):
        if lang != self.current_lang:
            self.load_translations(lang)

    def get_text(self, key):
        # Returns the translated text, or the key itself if not found
        return self.translations.get(key, key)

# Singleton instance
loc = LocalizationManager()
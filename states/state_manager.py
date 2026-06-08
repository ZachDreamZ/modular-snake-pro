import pygame
import random
import math
from config import *
import game_assets
import ui
import save_manager
from entities import Snake, AISnake, Food, Particle, Boss, Projectile
from .state_menu import MenuState
from .state_shop import ShopState
from .state_gameplay import GameplayState
from localization_manager import loc

class StateManager:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.state_name = "MENU"
        self.unlocked_themes = game_assets.load_unlocked_themes()
        self.theme = THEMES[self.unlocked_themes[0]] if self.unlocked_themes else THEMES["default"]
        self.running = True

        self.bg_surface = self._generate_bg_surface()

        self.shop_index = 0
        self.theme_costs = {"default": 0, "dark": 50, "neon": 100, "golden_mecha": 0, "ghost": 0, "void": 200}
        self.theme_keys = ["default", "dark", "neon", "golden_mecha", "ghost", "void"]

        self.snake = None
        self.ai_snake = None
        self.food = None
        self.particles = []
        self.score = 0
        self.stage = 1
        self.food_eaten_this_stage = 0
        self.total_food_eaten = 0
        self.obstacles = []
        self.game_speed = 10
        self.shield_timer = 0
        self.invulnerability_timer = 0
        self.combo_count = 0
        self.combo_timer = 0
        self.ghost_timer = 0
        self.frenzy_timer = 0
        self.highscore = game_assets.load_high_score()
        self.total_points = game_assets.load_total_points()

        self.boss = None
        self.projectiles = []
        self.boss_hazards = []
        self.shake_amount = 0
        self.victory_timer = 0
        self.boss_wins = 0

        self.player_name = ["A", "A", "A"]
        self.name_cursor = 0

        self.current_mode = MODE_CLASSIC
        self.time_rush_timer = 0
        self.survival_timer = 0

        self.settings = game_assets.load_settings()
        game_assets.sound_manager.set_music(self.settings.get("music", True))
        game_assets.sound_manager.set_sfx(self.settings.get("sfx", True))
        loc.set_language(self.settings.get("language", "en"))

        self.unlocked_achievements = game_assets.load_achievements()
        self.active_toast = None
        self.toast_timer = 0
        self.toast_offset_y = -50

        self.objectives_progress = save_manager.load_objectives_progress()
        self.completed_objectives = self.objectives_progress.get("completed", [])

        self.stats = save_manager.load_stats()
        self.boss_wins = self.stats.get("boss_wins", 0)
        self.games_played = self.stats.get("games_played", 0)

        self.countdown_timer = 0
        self.countdown_text = ""

        self.menu_snake = AISnake((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        try:
            self.pixel_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", FONT_SIZE_MEDIUM)
            self.title_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", FONT_SIZE_HUGE)
            self.small_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", FONT_SIZE_TINY)
        except Exception as e:
            print(f"Font loading failed: {e}")
            self.pixel_font = pygame.font.SysFont("Arial", FONT_SIZE_MEDIUM, bold=True)
            self.title_font = pygame.font.SysFont("Arial", FONT_SIZE_HUGE, bold=True)
            self.small_font = pygame.font.SysFont("Arial", FONT_SIZE_TINY, bold=True)

        self.menu_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.menu_overlay.fill((0, 0, 0, 150))

        self.shop_ui = ui.ShopUI()

        game_assets.sound_manager.play_music("assets/bgm_main.wav")

        self._build_menu_buttons()

        self.title_surf = self.title_font.render("SNAKE GRADIENT", True, COLOR_WHITE)

        self.hints_shown = set()
        self.hint_timers = {}
        self.active_hints = []
        self.total_game_time = 0

        self.states = {
            "MENU": MenuState(),
            "SHOP": ShopState(),
            "PLAYING": GameplayState()
        }
        self.current_state_obj = self.states["MENU"]

    def _generate_bg_surface(self):
        bg = pygame.Surface((SCREEN_WIDTH + BLOCK_SIZE * 2, SCREEN_HEIGHT + BLOCK_SIZE * 2))
        c1 = self.theme.get("bg_color", COLOR_BLACK)
        c2 = tuple(max(10, min(255, c + 30)) for c in c1)
        for x in range(0, SCREEN_WIDTH + BLOCK_SIZE * 2, BLOCK_SIZE):
            for y in range(0, SCREEN_HEIGHT + BLOCK_SIZE * 2, BLOCK_SIZE):
                color = c1 if (x // BLOCK_SIZE + y // BLOCK_SIZE) % 2 == 0 else c2
                pygame.draw.rect(bg, color, (x, y, BLOCK_SIZE, BLOCK_SIZE))
        return bg

    def _build_menu_buttons(self):
        self.menu_buttons = [
            ui.Button(loc.get_text("menu_play"), SCREEN_WIDTH // 2, 200, 200, 50, (57, 255, 20), (150, 255, 100), self.pixel_font, "click", key="menu_play"),
            ui.Button(loc.get_text("menu_shop"), 300, 260, 180, 50, (112, 128, 144), (160, 170, 180), self.pixel_font, "click", key="menu_shop"),
            ui.Button(loc.get_text("menu_settings"), 500, 260, 180, 50, (112, 128, 144), (160, 170, 180), self.pixel_font, "click", key="menu_settings"),
            ui.Button(loc.get_text("menu_leaderboard"), SCREEN_WIDTH // 2, 320, 200, 50, (112, 128, 144), (160, 170, 180), self.pixel_font, "click", key="menu_leaderboard"),
        ]

    @property
    def state(self):
        return self.state_name

    @state.setter
    def state(self, value):
        self.state_name = value
        if value == "MENU" or value == "MODE_SELECT" or value == "SETTINGS" or value == "LEADERBOARD":
            self.current_state_obj = self.states["MENU"]
        elif value == "SHOP":
            self.current_state_obj = self.states["SHOP"]
        elif value in ["PLAYING", "PAUSED", "GAMEOVER", "COUNTDOWN", "BOSS_BATTLE", "VICTORY", "HIGH_SCORE_ENTRY"]:
            self.current_state_obj = self.states["PLAYING"]

    def change_state(self, new_state):
        self.state = new_state

    def reset_game(self):
        mode_cfg = GAME_MODES[self.current_mode]
        self.snake = Snake((BLOCK_SIZE * 5, BLOCK_SIZE * 5), self.theme["snake_color"], self.theme["snake_color_dark"])
        self.ai_snake = AISnake((BLOCK_SIZE * 15, BLOCK_SIZE * 15))
        self.food = Food()
        self.stage = mode_cfg["start_stage"]
        self.food_eaten_this_stage = 0
        self.obstacles = []

        self.update_stage()

        self.food.spawn(self.snake.body, self.ai_snake.body, self.obstacles)
        self.particles = []
        self.score = 0
        self.game_speed = mode_cfg["base_speed"]
        self.time_rush_timer = mode_cfg["timer"] if mode_cfg["timer"] else 0
        self.survival_timer = 0
        self.combo_count = 0
        self.combo_timer = 0
        self.ghost_timer = 0
        self.frenzy_timer = 0
        self.shield_timer = 0
        self.invulnerability_timer = 0
        self.games_played += 1

        self.active_hints = []
        self.hint_timers = {}
        self.total_game_time = 0

    def start_countdown(self):
        self.countdown_timer = 180
        self.change_state("COUNTDOWN")

    def trigger_toast(self, message):
        self.active_toast = message
        self.toast_timer = 180
        self.toast_offset_y = -50

    def update_stage(self):
        if self.food_eaten_this_stage >= 5:
            self.stage += 1
            self.food_eaten_this_stage = 0
            self.obstacles = []
            if self.stage == 5:
                self.start_boss_battle()
                return
            if self.stage == 2:
                gap_x = SCREEN_WIDTH // 2
                for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
                    if not (gap_x - BLOCK_SIZE <= x <= gap_x):
                        self.obstacles.append((x, SCREEN_HEIGHT // 2))
            elif self.stage >= 3:
                corners = [(0,0), (SCREEN_WIDTH-BLOCK_SIZE,0), (0,SCREEN_HEIGHT-BLOCK_SIZE), (SCREEN_WIDTH-BLOCK_SIZE, SCREEN_HEIGHT-BLOCK_SIZE)]
                for cx, cy in corners:
                    for dx in range(3):
                        for dy in range(3):
                            tx = cx + dx * BLOCK_SIZE if cx == 0 else cx - dx * BLOCK_SIZE
                            ty = cy + dy * BLOCK_SIZE if cy == 0 else cy - dy * BLOCK_SIZE
                            if 0 <= tx < SCREEN_WIDTH and 0 <= ty < SCREEN_HEIGHT:
                                if dx == 0 or dx == 2 or dy == 0 or dy == 2:
                                    self.obstacles.append((tx, ty))

    def start_boss_battle(self):
        self.change_state("BOSS_BATTLE")
        self.boss = Boss((SCREEN_WIDTH // 2, BLOCK_SIZE))
        self.obstacles = []
        self.boss_hazards = []
        self.projectiles = []
        self.food.spawn(self.snake.body, [], self.obstacles, self.boss.body)

    def handle_events(self, events):
        self.current_state_obj.handle_events(self, events)

    def show_contextual_hint(self, hint_key, text, duration):
        if hint_key not in self.hints_shown:
            self.hints_shown.add(hint_key)
            self.active_hints.append({"text": text, "timer": duration, "alpha": 255})

    def update(self):
        if self.shake_amount > 0:
            self.shake_amount -= 1

        if self.active_toast:
            if self.toast_timer > 0:
                self.toast_timer -= 1
                if self.toast_offset_y < 0:
                    self.toast_offset_y += 2
            else:
                self.toast_offset_y -= 2
                if self.toast_offset_y < -100:
                    self.active_toast = None
                    self.toast_offset_y = -50

        for hint in self.active_hints[:]:
            hint["timer"] -= 1
            if hint["timer"] <= 0:
                self.active_hints.remove(hint)

        self.current_state_obj.update(self)

    def draw(self):
        offset_x = random.randint(-self.shake_amount, self.shake_amount) if self.shake_amount > 0 else 0
        offset_y = random.randint(-self.shake_amount, self.shake_amount) if self.shake_amount > 0 else 0
        bg_offset_x = (pygame.time.get_ticks() * 0.02) % BLOCK_SIZE
        bg_offset_y = (pygame.time.get_ticks() * 0.01) % BLOCK_SIZE
        self.screen.blit(self.bg_surface, (offset_x - bg_offset_x, offset_y - bg_offset_y))
        self.screen.blit(self.bg_surface, (offset_x - bg_offset_x + SCREEN_WIDTH, offset_y - bg_offset_y))
        self.screen.blit(self.bg_surface, (offset_x - bg_offset_x, offset_y - bg_offset_y + SCREEN_HEIGHT))
        self.screen.blit(self.bg_surface, (offset_x - bg_offset_x + SCREEN_WIDTH, offset_y - bg_offset_y + SCREEN_HEIGHT))

        self.current_state_obj.draw(self, offset_x, offset_y)

        # Subtle vignette overlay
        if self.state not in ("MENU", "MODE_SELECT", "SETTINGS", "LEADERBOARD", "SHOP"):
            vignette = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            for r in range(SCREEN_WIDTH // 2, 0, -1):
                alpha = max(0, 30 - r)
                pygame.draw.circle(vignette, (0, 0, 0, alpha), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), r)
            self.screen.blit(vignette, (0, 0))

        for i, hint in enumerate(self.active_hints):
            hint_y = SCREEN_HEIGHT - 60 - (len(self.active_hints) - 1 - i) * 25
            hint_alpha = min(255, hint["timer"] * 2) if hint["timer"] < 60 else 255
            font_size = FONT_SIZE_TINY
            try:
                adjusted_size = int(font_size * self.settings.get("font_scale", 1.0))
                hint_font = pygame.font.SysFont("Arial", adjusted_size, bold=True)
                text_surf = hint_font.render(hint["text"], True, (200, 200, 100))
                text_surf.set_alpha(hint_alpha)
                text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, hint_y))
                self.screen.blit(text_surf, text_rect)
            except Exception:
                pass

        if self.active_toast:
            toast_w, toast_h = 350, 50
            tx = SCREEN_WIDTH - toast_w - 20
            ty = 20 + self.toast_offset_y
            ui.draw_panel(self.screen, tx, ty, toast_w, toast_h, alpha=180)
            ui.draw_text(self.screen, f"🏆 {self.active_toast}", FONT_SIZE_SMALL, tx + toast_w // 2, ty + toast_h // 2, COLOR_YELLOW)

    def save_persistent_stats(self):
        self.stats["total_food_eaten"] = self.stats.get("total_food_eaten", 0) + self.total_food_eaten
        self.stats["boss_wins"] = self.boss_wins
        self.stats["games_played"] = self.games_played
        self.stats["max_combo"] = max(self.stats.get("max_combo", 0), self.combo_count)
        save_manager.save_stats(self.stats)

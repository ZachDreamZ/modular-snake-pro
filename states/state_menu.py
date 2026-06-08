import random
import math
import pygame
from config import *
import game_assets
import ui
from localization_manager import loc

class MenuState:
    def __init__(self):
        self.sub_state = "MENU"
        self.particles = []
        self._starfield = None
        self._star_surf = None
        self._scroll = 0

    def _init_stars(self):
        if self._starfield is None or len(self._starfield) == 0:
            self._starfield = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(1, 3), random.randint(20, 100)) for _ in range(60)]

    def handle_events(self, manager, events):
        mx, my = pygame.mouse.get_pos()

        if self.sub_state == "MENU":
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in manager.menu_buttons:
                        if btn.rect.collidepoint(mx, my):
                            if btn.key == "menu_play":
                                manager.change_state("MODE_SELECT")
                                self.sub_state = "MODE_SELECT"
                                self._clear_sub_buttons()
                            elif btn.key == "menu_shop":
                                manager.change_state("SHOP")
                            elif btn.key == "menu_settings":
                                manager.change_state("SETTINGS")
                                self.sub_state = "SETTINGS"
                                self._clear_sub_buttons()
                            elif btn.key == "menu_leaderboard":
                                manager.change_state("LEADERBOARD")
                                self.sub_state = "LEADERBOARD"
                                self._clear_sub_buttons()

        elif self.sub_state == "MODE_SELECT":
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in self.mode_buttons:
                        if btn.rect.collidepoint(mx, my):
                            if btn.key == "mode_classic": manager.current_mode = MODE_CLASSIC
                            elif btn.key == "mode_time_rush": manager.current_mode = MODE_TIME_RUSH
                            elif btn.key == "mode_maze_hell": manager.current_mode = MODE_MAZE_HELL
                            manager.reset_game()
                            manager.start_countdown()
                            self.sub_state = "MENU"
                            manager.change_state("COUNTDOWN")
                    if self.back_btn and self.back_btn.rect.collidepoint(mx, my):
                        self.sub_state = "MENU"
                        manager.change_state("MENU")

        elif self.sub_state == "SETTINGS":
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.music_btn.rect.collidepoint(mx, my):
                        manager.settings["music"] = not manager.settings["music"]
                        game_assets.sound_manager.set_music(manager.settings["music"])
                        game_assets.save_settings(manager.settings)
                    elif self.sfx_btn.rect.collidepoint(mx, my):
                        manager.settings["sfx"] = not manager.settings["sfx"]
                        game_assets.sound_manager.set_sfx(manager.settings["sfx"])
                        game_assets.save_settings(manager.settings)
                    elif self.font_btn.rect.collidepoint(mx, my):
                        scales = [1.0, 1.2, 1.5]
                        current = manager.settings.get("font_scale", 1.0)
                        next_scale = scales[(scales.index(current) + 1) % len(scales)]
                        manager.settings["font_scale"] = next_scale
                        game_assets.save_settings(manager.settings)
                    elif self.cb_btn.rect.collidepoint(mx, my):
                        modes = ["none", "protanopia", "deuteranopia", "tritanopia"]
                        current = manager.settings.get("colorblind", "none")
                        next_mode = modes[(modes.index(current) + 1) % len(modes)]
                        manager.settings["colorblind"] = next_mode
                        game_assets.save_settings(manager.settings)
                    elif self.lang_btn.rect.collidepoint(mx, my):
                        langs = ["en", "es", "fr"]
                        current = manager.settings.get("language", "en")
                        next_lang = langs[(langs.index(current) + 1) % len(langs)]
                        manager.settings["language"] = next_lang
                        loc.set_language(next_lang)
                        game_assets.save_settings(manager.settings)
                        manager._build_menu_buttons()
                    elif self.back_btn.rect.collidepoint(mx, my):
                        self.sub_state = "MENU"
                        manager.change_state("MENU")

        elif self.sub_state == "LEADERBOARD":
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.stats_btn and self.stats_btn.rect.collidepoint(mx, my):
                        self.sub_state = "STATS"
                    elif self.back_btn and self.back_btn.rect.collidepoint(mx, my):
                        self.sub_state = "MENU"
                        manager.change_state("MENU")

        elif self.sub_state == "STATS":
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.ach_btn and self.ach_btn.rect.collidepoint(mx, my):
                        self.sub_state = "ACHIEVEMENTS"
                    elif self.obj_btn and self.obj_btn.rect.collidepoint(mx, my):
                        self.sub_state = "OBJECTIVES"
                    elif self.back_btn and self.back_btn.rect.collidepoint(mx, my):
                        self.sub_state = "LEADERBOARD"

        elif self.sub_state == "ACHIEVEMENTS":
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_btn and self.back_btn.rect.collidepoint(mx, my):
                        self.sub_state = "STATS"

        elif self.sub_state == "OBJECTIVES":
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_btn and self.back_btn.rect.collidepoint(mx, my):
                        self.sub_state = "STATS"

    def _clear_sub_buttons(self):
        for attr in ("mode_buttons", "back_btn", "music_btn", "sfx_btn", "font_btn", "cb_btn", "lang_btn", "stats_btn", "ach_btn", "obj_btn"):
            if hasattr(self, attr):
                delattr(self, attr)

    def update(self, manager):
        self._init_stars()
        if self.sub_state == "MENU":
            if hasattr(manager, 'menu_snake'):
                manager.menu_snake.update()
            self._scroll = (self._scroll + 0.3) % SCREEN_HEIGHT
            if len(self.particles) < 40:
                self.particles.append({
                    "pos": [random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT + 5],
                    "vel": [random.uniform(-0.3, 0.3), random.uniform(-0.8, -0.2)],
                    "size": random.randint(1, 3),
                    "alpha": random.randint(30, 100),
                    "color": random.choice([(57, 255, 20), (100, 200, 255), (255, 215, 0), (255, 100, 100)])
                })
            for p in self.particles[:]:
                p["pos"][0] += p["vel"][0]
                p["pos"][1] += p["vel"][1]
                if p["pos"][1] < -10:
                    self.particles.remove(p)

    def draw(self, manager, offset_x, offset_y):
        if self.sub_state == "MENU":
            self._draw_menu(manager, offset_x, offset_y)
        elif self.sub_state == "MODE_SELECT":
            self.draw_mode_select(manager)
        elif self.sub_state == "SETTINGS":
            self.draw_settings(manager)
        elif self.sub_state == "LEADERBOARD":
            self.draw_leaderboard(manager)
        elif self.sub_state == "STATS":
            self.draw_stats(manager)
        elif self.sub_state == "ACHIEVEMENTS":
            self.draw_achievements(manager)
        elif self.sub_state == "OBJECTIVES":
            self.draw_objectives(manager)

    def _draw_menu(self, manager, offset_x, offset_y):
        self._init_stars()
        for sx, sy, sz, sa in self._starfield:
            adj_y = (sy + self._scroll) % SCREEN_HEIGHT
            surf = pygame.Surface((sz * 2, sz * 2), pygame.SRCALPHA)
            alpha = int(sa * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() * 0.001 + sx)))
            pygame.draw.circle(surf, (255, 255, 255, alpha), (sz, sz), sz)
            manager.screen.blit(surf, (sx, adj_y))

        manager.screen.blit(manager.menu_overlay, (0, 0))

        # Particles
        for p in self.particles:
            surf = pygame.Surface((p["size"] * 2, p["size"] * 2), pygame.SRCALPHA)
            c = p["color"] + (p["alpha"],)
            pygame.draw.circle(surf, c, (p["size"], p["size"]), p["size"])
            manager.screen.blit(surf, (int(p["pos"][0]), int(p["pos"][1])))

        # Top score banner
        banner_rect = pygame.Rect(SCREEN_WIDTH // 2 - 140, 12, 280, 28)
        pygame.draw.rect(manager.screen, (20, 20, 30, 180), banner_rect, border_radius=14)
        pygame.draw.rect(manager.screen, COLOR_GOLD, banner_rect, 1, border_radius=14)
        import save_manager
        top_score = save_manager.get_high_score()
        ui.draw_text(manager.screen, f"BEST: {top_score}", FONT_SIZE_TINY, SCREEN_WIDTH // 2, 26, COLOR_GOLD, manager.small_font)

        # Title with glow
        t = pygame.time.get_ticks() / 1000
        title_y = 95 + math.sin(t * 0.5) * 3
        title_rect = pygame.Rect(SCREEN_WIDTH // 2 - 230, int(title_y) - 35, 460, 70)

        # Title background panel
        pygame.draw.rect(manager.screen, (0, 0, 0, 120), title_rect, border_radius=15)
        pygame.draw.rect(manager.screen, (60, 60, 60, 100), title_rect, 1, border_radius=15)

        # Glow behind title text
        for r in range(8, 0, -1):
            glow_sz = manager.title_surf.get_width() + r * 8
            glow_surf = pygame.Surface((glow_sz, 60), pygame.SRCALPHA)
            alpha = max(0, 30 - r * 3)
            pygame.draw.rect(glow_surf, (57, 255, 20, alpha), glow_surf.get_rect(), border_radius=10)
            gx = SCREEN_WIDTH // 2 - glow_sz // 2
            gy = int(title_y) - 30
            manager.screen.blit(glow_surf, (gx, gy))

        manager.screen.blit(manager.title_surf, (SCREEN_WIDTH // 2 - manager.title_surf.get_width() // 2, int(title_y) - 20))

        # Decorative line under title
        line_y = int(title_y) + 25
        line_w = 300 + math.sin(t * 0.7) * 20
        line_rect = pygame.Rect(SCREEN_WIDTH // 2 - line_w // 2, line_y, line_w, 2)
        pygame.draw.rect(manager.screen, (57, 255, 20), line_rect, border_radius=1)

        # Version
        ui.draw_text(manager.screen, f"v{VERSION}", FONT_SIZE_TINY, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 15, COLOR_GREY, manager.small_font)

        # Buttons
        for btn in manager.menu_buttons:
            btn.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
            btn.draw(manager.screen)

        # Menu snake
        if hasattr(manager, 'menu_snake'):
            for i, seg in enumerate(manager.menu_snake.body):
                color = manager.theme["snake_color"] if i == 0 else manager.theme["snake_color_dark"]
                pygame.draw.rect(manager.screen, color, (*seg, BLOCK_SIZE, BLOCK_SIZE))

    def draw_mode_select(self, manager):
        manager.screen.blit(manager.menu_overlay, (0, 0))
        ui.draw_glow_text(manager.screen, loc.get_text("mode_select"), FONT_SIZE_MEDIUM, SCREEN_WIDTH // 2, 85, COLOR_WHITE, manager.pixel_font)

        self.mode_buttons = [
            ui.Button(loc.get_text("mode_classic"), SCREEN_WIDTH // 2, 170, 250, 45, (57, 255, 20), (100, 255, 80), manager.pixel_font, "click", key="mode_classic"),
            ui.Button(loc.get_text("mode_time_rush"), SCREEN_WIDTH // 2, 230, 250, 45, (112, 128, 144), (160, 170, 180), manager.pixel_font, "click", key="mode_time_rush"),
            ui.Button(loc.get_text("mode_maze_hell"), SCREEN_WIDTH // 2, 290, 250, 45, (200, 50, 50), (240, 80, 80), manager.pixel_font, "click", key="mode_maze_hell"),
        ]
        self.back_btn = ui.Button(loc.get_text("common_back"), SCREEN_WIDTH // 2, 355, 150, 35, (80, 80, 80), (120, 120, 120), manager.small_font, "click", key="back")

        for btn in self.mode_buttons:
            btn.draw(manager.screen)
        if hasattr(self, 'back_btn') and self.back_btn:
            self.back_btn.draw(manager.screen)

    def draw_settings(self, manager):
        manager.screen.blit(manager.menu_overlay, (0, 0))
        ui.draw_glow_text(manager.screen, loc.get_text("settings_title"), FONT_SIZE_MEDIUM, SCREEN_WIDTH // 2, 85, COLOR_WHITE, manager.pixel_font)

        self.music_btn = ui.Button(loc.get_text("settings_music_on" if manager.settings.get("music") else "settings_music_off"), SCREEN_WIDTH // 2, 125, 240, 32, (60, 60, 60), (90, 90, 90), manager.small_font, "click", key="music")
        self.sfx_btn = ui.Button(loc.get_text("settings_sfx_on" if manager.settings.get("sfx") else "settings_sfx_off"), SCREEN_WIDTH // 2, 165, 240, 32, (60, 60, 60), (90, 90, 90), manager.small_font, "click", key="sfx")
        self.font_btn = ui.Button(f"Font: {manager.settings.get('font_scale', 1.0)}x", SCREEN_WIDTH // 2, 205, 240, 32, (60, 60, 60), (90, 90, 90), manager.small_font, "click", key="font")
        self.cb_btn = ui.Button(f"Colorblind: {manager.settings.get('colorblind', 'none')}", SCREEN_WIDTH // 2, 245, 240, 32, (60, 60, 60), (90, 90, 90), manager.small_font, "click", key="colorblind")
        self.lang_btn = ui.Button(f"Lang: {manager.settings.get('language', 'en').upper()}", SCREEN_WIDTH // 2, 285, 240, 32, (60, 60, 60), (90, 90, 90), manager.small_font, "click", key="language")
        self.back_btn = ui.Button(loc.get_text("common_back"), SCREEN_WIDTH // 2, 345, 140, 32, (120, 40, 40), (160, 60, 60), manager.small_font, "click", key="back")

        self.music_btn.text = loc.get_text("settings_music_on" if manager.settings.get("music") else "settings_music_off")
        self.sfx_btn.text = loc.get_text("settings_sfx_on" if manager.settings.get("sfx") else "settings_sfx_off")
        self.font_btn.text = f"Font: {manager.settings.get('font_scale', 1.0)}x"
        self.cb_btn.text = f"Colorblind: {manager.settings.get('colorblind', 'none')}"
        self.lang_btn.text = f"Lang: {manager.settings.get('language', 'en').upper()}"

        self.music_btn.draw(manager.screen)
        self.sfx_btn.draw(manager.screen)
        self.font_btn.draw(manager.screen)
        self.cb_btn.draw(manager.screen)
        self.lang_btn.draw(manager.screen)
        self.back_btn.draw(manager.screen)

    def draw_leaderboard(self, manager):
        manager.screen.blit(manager.menu_overlay, (0, 0))
        ui.draw_glow_text(manager.screen, loc.get_text("leaderboard_title"), FONT_SIZE_MEDIUM, SCREEN_WIDTH // 2, 85, COLOR_GOLD, manager.pixel_font)

        high_scores = game_assets.load_leaderboard()
        for i, entry in enumerate(high_scores[:5]):
            name = entry.get("name", "Unknown")
            score = entry.get("score", 0)
            stage = entry.get("stage", 1)
            rank_colors = [COLOR_GOLD, (200, 200, 200), (180, 120, 60), COLOR_GREY, COLOR_GREY]
            c = rank_colors[i] if i < len(rank_colors) else COLOR_GREY
            ui.draw_text(manager.screen, f"{i+1}. {name}  {score} (St.{stage})", FONT_SIZE_SMALL, SCREEN_WIDTH // 2, 145 + i * 32, c, manager.small_font)

        if not high_scores:
            ui.draw_text(manager.screen, "No scores yet!", FONT_SIZE_SMALL, SCREEN_WIDTH // 2, 200, COLOR_GREY, manager.small_font)

        self.stats_btn = ui.Button(loc.get_text("btn_stats"), SCREEN_WIDTH // 2 - 80, 330, 130, 35, (57, 255, 20), (100, 255, 80), manager.small_font, "click", key="stats")
        self.back_btn = ui.Button(loc.get_text("common_back"), SCREEN_WIDTH // 2 + 80, 330, 130, 35, (120, 40, 40), (160, 60, 60), manager.small_font, "click", key="back")

        self.stats_btn.draw(manager.screen)
        self.back_btn.draw(manager.screen)

    def draw_stats(self, manager):
        manager.screen.blit(manager.menu_overlay, (0, 0))
        ui.draw_glow_text(manager.screen, loc.get_text("stats_title"), FONT_SIZE_MEDIUM, SCREEN_WIDTH // 2, 85, COLOR_WHITE, manager.pixel_font)

        stats = manager.stats
        labels = [
            (loc.get_text("games_played_label"), f"{stats.get('games_played', 0)}", COLOR_WHITE),
            (loc.get_text("boss_wins_label"), f"{stats.get('boss_wins', 0)}", COLOR_BOSS_GOLD),
            (loc.get_text("total_food_eaten_label"), f"{stats.get('total_food_eaten', 0)}", COLOR_GREEN),
            (loc.get_text("max_combo_label"), f"{stats.get('max_combo', 0)}x", COLOR_YELLOW),
        ]
        y = 145
        for label, value, val_color in labels:
            ui.draw_text(manager.screen, label + value, FONT_SIZE_SMALL, SCREEN_WIDTH // 2, y, val_color, manager.small_font)
            y += 30
        ui.draw_text(manager.screen, f"Points: {manager.total_points}", FONT_SIZE_SMALL, SCREEN_WIDTH // 2, y, COLOR_GOLD, manager.small_font)

        self.ach_btn = ui.Button(loc.get_text("btn_achievements"), SCREEN_WIDTH // 2 - 120, 325, 110, 32, (120, 30, 180), (160, 60, 220), manager.small_font, "click", key="achievements")
        self.obj_btn = ui.Button(loc.get_text("btn_objectives"), SCREEN_WIDTH // 2, 325, 110, 32, (180, 150, 0), (220, 200, 30), manager.small_font, "click", key="objectives")
        self.back_btn = ui.Button(loc.get_text("common_back"), SCREEN_WIDTH // 2 + 120, 325, 110, 32, (120, 40, 40), (160, 60, 60), manager.small_font, "click", key="back")

        self.ach_btn.draw(manager.screen)
        self.obj_btn.draw(manager.screen)
        self.back_btn.draw(manager.screen)

    def draw_achievements(self, manager):
        manager.screen.blit(manager.menu_overlay, (0, 0))
        ui.draw_glow_text(manager.screen, loc.get_text("achievements_title"), FONT_SIZE_MEDIUM, SCREEN_WIDTH // 2, 85, (160, 32, 240), manager.pixel_font)

        y = 135
        unlocked = manager.unlocked_achievements
        for key, defn in ACHIEVEMENT_DEFS.items():
            is_unlocked = key in unlocked or defn["name"] in unlocked
            color = COLOR_GREEN if is_unlocked else COLOR_GREY
            prefix = "✓" if is_unlocked else "✗"
            display_name = defn["name"] if isinstance(defn, dict) and "name" in defn else key
            ui.draw_text(manager.screen, f"{prefix} {display_name}", FONT_SIZE_TINY, SCREEN_WIDTH // 2, y, color, manager.small_font)
            y += 22

        self.back_btn = ui.Button(loc.get_text("common_back"), SCREEN_WIDTH // 2, 340, 130, 32, (120, 40, 40), (160, 60, 60), manager.small_font, "click", key="back")
        self.back_btn.draw(manager.screen)

    def draw_objectives(self, manager):
        manager.screen.blit(manager.menu_overlay, (0, 0))
        ui.draw_glow_text(manager.screen, loc.get_text("objectives_title"), FONT_SIZE_MEDIUM, SCREEN_WIDTH // 2, 85, (255, 215, 0), manager.pixel_font)

        y = 135
        completed = manager.completed_objectives
        for key, defn in OBJECTIVE_DEFS.items():
            is_complete = key in completed
            color = COLOR_GREEN if is_complete else COLOR_GREY
            prefix = "✓" if is_complete else "☐"
            reward = defn.get("reward", 0)
            ui.draw_text(manager.screen, f"{prefix} {defn['name']} ({reward} pts)", FONT_SIZE_TINY, SCREEN_WIDTH // 2, y, color, manager.small_font)
            y += 22

        self.back_btn = ui.Button(loc.get_text("common_back"), SCREEN_WIDTH // 2, 340, 130, 32, (120, 40, 40), (160, 60, 60), manager.small_font, "click", key="back")
        self.back_btn.draw(manager.screen)

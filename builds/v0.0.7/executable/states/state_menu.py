import random
import pygame
from config import *
import game_assets
import ui
from localization_manager import loc

class MenuState:
    def __init__(self):
        self.sub_state = "MENU"
        self.particles = []

    def handle_events(self, manager, events):
        mx, my = pygame.mouse.get_pos()
        
        if self.sub_state == "MENU":
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in manager.menu_buttons:
                        if btn.rect.collidepoint(mx, my):
                            if btn.text == loc.get_text("menu_play"):
                                manager.change_state("MODE_SELECT")
                                self.sub_state = "MODE_SELECT"
                            elif btn.text == loc.get_text("menu_shop"):
                                manager.change_state("SHOP")
                            elif btn.text == loc.get_text("menu_settings"):
                                manager.change_state("SETTINGS")
                                self.sub_state = "SETTINGS"
                            elif btn.text == loc.get_text("menu_leaderboard"):
                                manager.change_state("LEADERBOARD")
                                self.sub_state = "LEADERBOARD"
        
        elif self.sub_state == "MODE_SELECT":
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in self.mode_buttons:
                        if btn.rect.collidepoint(mx, my):
                            text = btn.text
                            if text == loc.get_text("mode_classic"): manager.current_mode = MODE_CLASSIC
                            elif text == loc.get_text("mode_time_rush"): manager.current_mode = MODE_TIME_RUSH
                            elif text == loc.get_text("mode_maze_hell"): manager.current_mode = MODE_MAZE_HELL
                            
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

    def update(self, manager):
        if self.sub_state == "MENU":
            if hasattr(manager, 'menu_snake'):
                manager.menu_snake.update()
            
            if len(self.particles) < 30:
                self.particles.append({
                    "pos": [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)],
                    "vel": [random.uniform(-0.5, 0.5), random.uniform(-1.0, -0.2)],
                    "size": random.randint(2, 5),
                    "alpha": random.randint(50, 150)
                })
            
            for p in self.particles[:]:
                p["pos"][0] += p["vel"][0]
                p["pos"][1] += p["vel"][1]
                if p["pos"][1] < -10:
                    self.particles.remove(p)

    def draw(self, manager, offset_x, offset_y):
        if self.sub_state == "MENU":
            manager.screen.blit(manager.menu_overlay, (0, 0))
            
            for p in self.particles:
                p_surf = pygame.Surface((p["size"]*2, p["size"]*2), pygame.SRCALPHA)
                pygame.draw.circle(p_surf, (255, 255, 255, p["alpha"]), (p["size"], p["size"]), p["size"])
                manager.screen.blit(p_surf, (p["pos"][0], p["pos"][1]))

            banner_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 30, 300, 40)
            pygame.draw.rect(manager.screen, (40, 40, 40), banner_rect, border_radius=20)
            pygame.draw.rect(manager.screen, COLOR_GOLD if 'COLOR_GOLD' in globals() else (255, 215, 0), banner_rect, 2, border_radius=20)
            
            import save_manager
            top_score = save_manager.get_high_score()
            ui.draw_text(manager.screen, f"TOP SCORE: {top_score}", FONT_SIZE_TINY, SCREEN_WIDTH // 2, 50, COLOR_WHITE, manager.small_font)

            title_rect = pygame.Rect(SCREEN_WIDTH // 2 - 250, 80, 500, 100)
            pygame.draw.rect(manager.screen, (20, 20, 20, 150), title_rect, border_radius=15)
            pygame.draw.rect(manager.screen, (60, 60, 60), title_rect, 2, border_radius=15)
            
            manager.screen.blit(manager.title_surf, (SCREEN_WIDTH // 2 - manager.title_surf.get_width() // 2, 110))
            
            for btn in manager.menu_buttons:
                btn.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
                btn.draw(manager.screen)
            
            if hasattr(manager, 'menu_snake'):
                for i, seg in enumerate(manager.menu_snake.body):
                    color = manager.theme["snake_color"] if i == 0 else manager.theme["snake_color_dark"]
                    pygame.draw.rect(manager.screen, color, (*seg, BLOCK_SIZE, BLOCK_SIZE))
        
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

    def draw_mode_select(self, manager):
        manager.screen.blit(manager.menu_overlay, (0, 0))
        ui.draw_text(manager.screen, loc.get_text("mode_select"), FONT_SIZE_MEDIUM, SCREEN_WIDTH // 2, 100, COLOR_WHITE, manager.pixel_font)
        
        if not hasattr(self, 'mode_buttons') or not self.mode_buttons:
            self.mode_buttons = [
                ui.Button(loc.get_text("mode_classic"), SCREEN_WIDTH // 2, 180, 250, 50, (112, 128, 144), (160, 170, 180), manager.pixel_font, "click"),
                ui.Button(loc.get_text("mode_time_rush"), SCREEN_WIDTH // 2, 240, 250, 50, (112, 128, 144), (160, 170, 180), manager.pixel_font, "click"),
                ui.Button(loc.get_text("mode_maze_hell"), SCREEN_WIDTH // 2, 300, 250, 50, (112, 128, 144), (160, 170, 180), manager.pixel_font, "click"),
            ]
            self.back_btn = ui.Button(loc.get_text("common_back"), SCREEN_WIDTH // 2, 360, 150, 40, (180, 50, 50), (220, 80, 80), manager.small_font, "click")

        for btn in self.mode_buttons:
            btn.draw(manager.screen)
        if hasattr(self, 'back_btn') and self.back_btn:
            self.back_btn.draw(manager.screen)

    def draw_settings(self, manager):
        manager.screen.blit(manager.menu_overlay, (0, 0))
        ui.draw_text(manager.screen, loc.get_text("settings_title"), FONT_SIZE_MEDIUM, SCREEN_WIDTH // 2, 100, COLOR_WHITE, manager.pixel_font)
        
        if not hasattr(self, 'music_btn') or not self.music_btn:
            self.music_btn = ui.Button(loc.get_text("settings_music_on" if manager.settings.get("music") else "settings_music_off"), SCREEN_WIDTH // 2, 160, 250, 40, (112, 128, 144), (160, 170, 180), manager.pixel_font, "click")
            self.sfx_btn = ui.Button(loc.get_text("settings_sfx_on" if manager.settings.get("sfx") else "settings_sfx_off"), SCREEN_WIDTH // 2, 210, 250, 40, (112, 128, 144), (160, 170, 180), manager.pixel_font, "click")
            self.font_btn = ui.Button(f"Font Scale: {manager.settings.get('font_scale', 1.0)}x", SCREEN_WIDTH // 2, 260, 250, 40, (112, 128, 144), (160, 170, 180), manager.pixel_font, "click")
            self.cb_btn = ui.Button(f"Colorblind: {manager.settings.get('colorblind', 'none')}", SCREEN_WIDTH // 2, 310, 250, 40, (112, 128, 144), (160, 170, 180), manager.pixel_font, "click")
            self.lang_btn = ui.Button(f"Lang: {manager.settings.get('language', 'en').upper()}", SCREEN_WIDTH // 2, 360, 250, 40, (112, 128, 144), (160, 170, 180), manager.pixel_font, "click")
            self.back_btn = ui.Button(loc.get_text("common_back"), SCREEN_WIDTH // 2, 420, 150, 40, (180, 50, 50), (220, 80, 80), manager.small_font, "click")
        
        self.music_btn.text = loc.get_text("settings_music_on" if manager.settings.get("music") else "settings_music_off")
        self.sfx_btn.text = loc.get_text("settings_sfx_on" if manager.settings.get("sfx") else "settings_sfx_off")
        self.font_btn.text = f"Font Scale: {manager.settings.get('font_scale', 1.0)}x"
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
        ui.draw_text(manager.screen, loc.get_text("leaderboard_title"), FONT_SIZE_MEDIUM, SCREEN_WIDTH // 2, 100, COLOR_WHITE, manager.pixel_font)
        
        high_scores = game_assets.load_leaderboard()
        for i, entry in enumerate(high_scores[:5]):
            name = entry.get("name", "Unknown")
            score = entry.get("score", 0)
            stage = entry.get("stage", 1)
            ui.draw_text(manager.screen, f"{i+1}. {name}: {score} (Stage {stage})", FONT_SIZE_SMALL, SCREEN_WIDTH // 2, 160 + i * 30, COLOR_WHITE, manager.small_font)
        
        if not hasattr(self, 'stats_btn') or not self.stats_btn:
            self.stats_btn = ui.Button("Stats", SCREEN_WIDTH // 2 - 80, 320, 140, 40, (57, 255, 20), (150, 255, 100), manager.small_font, "click")
            self.back_btn = ui.Button("Back", SCREEN_WIDTH // 2 + 80, 320, 140, 40, (180, 50, 50), (220, 80, 80), manager.small_font, "click")
        
        if hasattr(self, 'stats_btn') and self.stats_btn:
            self.stats_btn.draw(manager.screen)
            self.back_btn.draw(manager.screen)

    def draw_stats(self, manager):
        manager.screen.blit(manager.menu_overlay, (0, 0))
        ui.draw_text(manager.screen, "STATS", FONT_SIZE_MEDIUM, SCREEN_WIDTH // 2, 100, COLOR_WHITE, manager.pixel_font)
        
        stats = manager.stats
        y = 160
        ui.draw_text(manager.screen, f"{loc.get_text('games_played_label')}{stats.get('games_played', 0)}", FONT_SIZE_SMALL, SCREEN_WIDTH // 2, y, COLOR_WHITE, manager.small_font)
        y += 30
        ui.draw_text(manager.screen, f"{loc.get_text('boss_wins_label')}{stats.get('boss_wins', 0)}", FONT_SIZE_SMALL, SCREEN_WIDTH // 2, y, COLOR_WHITE, manager.small_font)
        y += 30
        ui.draw_text(manager.screen, f"{loc.get_text('total_food_eaten_label')}{stats.get('total_food_eaten', 0)}", FONT_SIZE_SMALL, SCREEN_WIDTH // 2, y, COLOR_WHITE, manager.small_font)
        y += 30
        ui.draw_text(manager.screen, f"{loc.get_text('max_combo_label')}{stats.get('max_combo', 0)}x", FONT_SIZE_SMALL, SCREEN_WIDTH // 2, y, COLOR_WHITE, manager.small_font)
        y += 30
        ui.draw_text(manager.screen, f"Total Points: {manager.total_points}", FONT_SIZE_SMALL, SCREEN_WIDTH // 2, y, COLOR_GOLD, manager.small_font)
        
        if not hasattr(self, 'ach_btn') or not self.ach_btn:
            self.ach_btn = ui.Button("Achievements", SCREEN_WIDTH // 2 - 120, 330, 120, 40, (160, 32, 240), (200, 80, 255), manager.small_font, "click")
            self.obj_btn = ui.Button("Objectives", SCREEN_WIDTH // 2, 330, 120, 40, (255, 215, 0), (255, 255, 100), manager.small_font, "click")
            self.back_btn = ui.Button("Back", SCREEN_WIDTH // 2 + 120, 330, 120, 40, (180, 50, 50), (220, 80, 80), manager.small_font, "click")
        
        if hasattr(self, 'ach_btn') and self.ach_btn:
            self.ach_btn.draw(manager.screen)
            self.obj_btn.draw(manager.screen)
            self.back_btn.draw(manager.screen)

    def draw_achievements(self, manager):
        manager.screen.blit(manager.menu_overlay, (0, 0))
        ui.draw_text(manager.screen, loc.get_text("achievements_title"), FONT_SIZE_MEDIUM, SCREEN_WIDTH // 2, 100, COLOR_WHITE, manager.pixel_font)
        
        y = 150
        unlocked = manager.unlocked_achievements
        for key, defn in ACHIEVEMENT_DEFS.items():
            is_unlocked = key in unlocked or defn["name"] in unlocked
            color = COLOR_GREEN if is_unlocked else COLOR_GREY
            prefix = "✅" if is_unlocked else "🔒"
            display_name = defn["name"] if isinstance(defn, dict) and "name" in defn else key
            ui.draw_text(manager.screen, f"{prefix} {display_name}", FONT_SIZE_TINY, SCREEN_WIDTH // 2, y, color, manager.small_font)
            y += 25
        
        if not hasattr(self, 'back_btn') or not self.back_btn:
            self.back_btn = ui.Button("Back", SCREEN_WIDTH // 2, 340, 150, 40, (180, 50, 50), (220, 80, 80), manager.small_font, "click")
        
        if hasattr(self, 'back_btn') and self.back_btn:
            self.back_btn.draw(manager.screen)

    def draw_objectives(self, manager):
        manager.screen.blit(manager.menu_overlay, (0, 0))
        ui.draw_text(manager.screen, loc.get_text("objectives_title"), FONT_SIZE_MEDIUM, SCREEN_WIDTH // 2, 100, COLOR_WHITE, manager.pixel_font)
        
        y = 150
        completed = manager.completed_objectives
        for key, defn in OBJECTIVE_DEFS.items():
            is_complete = key in completed
            color = COLOR_GREEN if is_complete else COLOR_GREY
            prefix = "✅" if is_complete else "⬜"
            reward = defn.get("reward", 0)
            ui.draw_text(manager.screen, f"{prefix} {defn['name']} ({reward} pts)", FONT_SIZE_TINY, SCREEN_WIDTH // 2, y, color, manager.small_font)
            y += 25
        
        if not hasattr(self, 'back_btn') or not self.back_btn:
            self.back_btn = ui.Button("Back", SCREEN_WIDTH // 2, 340, 150, 40, (180, 50, 50), (220, 80, 80), manager.small_font, "click")
        
        if hasattr(self, 'back_btn') and self.back_btn:
            self.back_btn.draw(manager.screen)
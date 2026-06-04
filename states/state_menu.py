import pygame
from config import *
import assets
import ui

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
                            if btn.text == "PLAY":
                                manager.change_state("MODE_SELECT")
                                self.sub_state = "MODE_SELECT"
                            elif btn.text == "SHOP":
                                manager.change_state("SHOP")
                            elif btn.text == "SETTINGS":
                                manager.change_state("SETTINGS")
                                self.sub_state = "SETTINGS"
                            elif btn.text == "LEADERBOARD":
                                manager.change_state("LEADERBOARD")
                                self.sub_state = "LEADERBOARD"
        
        elif self.sub_state == "MODE_SELECT":
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in self.mode_buttons:
                        if btn.rect.collidepoint(mx, my):
                            manager.current_mode = btn.text.upper().replace(" ", "_")
                            if "RUSH" in btn.text: manager.current_mode = MODE_TIME_RUSH
                            if "HELL" in btn.text: manager.current_mode = MODE_MAZE_HELL
                            if "CLASSIC" in btn.text: manager.current_mode = MODE_CLASSIC
                            manager.reset_game()
                            manager.start_countdown()
                            self.sub_state = "MENU"
                            manager.change_state("COUNTDOWN")
                    
                    if self.back_btn.rect.collidepoint(mx, my):
                        self.sub_state = "MENU"
                        manager.change_state("MENU")

        elif self.sub_state == "SETTINGS":
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.music_btn.rect.collidepoint(mx, my):
                        manager.settings["music"] = not manager.settings["music"]
                        assets.sound_manager.set_music(manager.settings["music"])
                        assets.save_settings(manager.settings)
                    elif self.sfx_btn.rect.collidepoint(mx, my):
                        manager.settings["sfx"] = not manager.settings["sfx"]
                        assets.sound_manager.set_sfx(manager.settings["sfx"])
                        assets.save_settings(manager.settings)
                    elif self.back_btn.rect.collidepoint(mx, my):
                        self.sub_state = "MENU"
                        manager.change_state("MENU")

        elif self.sub_state == "LEADERBOARD":
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_btn.rect.collidepoint(mx, my):
                        self.sub_state = "MENU"
                        manager.change_state("MENU")

    def update(self, manager):
        if self.sub_state == "MENU":
            manager.menu_snake.update()
            
            # Ambient particle drift
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
            
            # 1. Draw ambient particles
            for p in self.particles:
                p_surf = pygame.Surface((p["size"]*2, p["size"]*2), pygame.SRCALPHA)
                pygame.draw.circle(p_surf, (255, 255, 255, p["alpha"]), (p["size"], p["size"]), p["size"])
                manager.screen.blit(p_surf, (p["pos"][0], p["pos"][1]))

            # 2. High Score Banner (Top)
            banner_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 30, 300, 40)
            pygame.draw.rect(manager.screen, (40, 40, 40), banner_rect, border_radius=20)
            pygame.draw.rect(manager.screen, COLOR_GOLD if 'COLOR_GOLD' in globals() else (255, 215, 0), banner_rect, 2, border_radius=20)
            
            top_score = manager.highscore if manager.highscore else 0
            ui.draw_text(manager.screen, f"TOP SCORE: {top_score}", FONT_SIZE_TINY, SCREEN_WIDTH // 2, 50, COLOR_WHITE, manager.small_font)

            # 3. Stylized Title Card
            title_rect = pygame.Rect(SCREEN_WIDTH // 2 - 250, 80, 500, 100)
            pygame.draw.rect(manager.screen, (20, 20, 20, 150), title_rect, border_radius=15)
            pygame.draw.rect(manager.screen, (60, 60, 60), title_rect, 2, border_radius=15)
            
            # Draw Title
            manager.screen.blit(manager.title_surf, (SCREEN_WIDTH // 2 - manager.title_surf.get_width() // 2, 110))
            
            # 4. Draw buttons
            for btn in manager.menu_buttons:
                # Ensure buttons update their hover/press state
                btn.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
                btn.draw(manager.screen)
            
            # Draw menu snake
            for i, seg in enumerate(manager.menu_snake.body):
                color = manager.theme["snake_color"] if i == 0 else manager.theme["snake_color_dark"]
                pygame.draw.rect(manager.screen, color, (*seg, BLOCK_SIZE, BLOCK_SIZE))
        
        elif self.sub_state == "MODE_SELECT":
            self.draw_mode_select(manager)
        elif self.sub_state == "SETTINGS":
            self.draw_settings(manager)
        elif self.sub_state == "LEADERBOARD":
            self.draw_leaderboard(manager)

    def draw_mode_select(self, manager):
        manager.screen.blit(manager.menu_overlay, (0, 0))
        ui.draw_text(manager.screen, "SELECT MODE", FONT_SIZE_MEDIUM, SCREEN_WIDTH // 2, 100, COLOR_WHITE, manager.pixel_font)
        
        if not hasattr(self, 'mode_buttons'):
            self.mode_buttons = [
                ui.Button("Classic", SCREEN_WIDTH // 2, 180, 250, 50, (112, 128, 144), (160, 170, 180), manager.pixel_font, "click"),
                ui.Button("Time Rush", SCREEN_WIDTH // 2, 240, 250, 50, (112, 128, 144), (160, 170, 180), manager.pixel_font, "click"),
                ui.Button("Maze Hell", SCREEN_WIDTH // 2, 300, 250, 50, (112, 128, 144), (160, 170, 180), manager.pixel_font, "click"),
            ]
            self.back_btn = ui.Button("Back", SCREEN_WIDTH // 2, 360, 150, 40, (180, 50, 50), (220, 80, 80), manager.small_font, "click")

        for btn in self.mode_buttons:
            btn.draw(manager.screen)
        self.back_btn.draw(manager.screen)

    def draw_settings(self, manager):
        manager.screen.blit(manager.menu_overlay, (0, 0))
        ui.draw_text(manager.screen, "SETTINGS", FONT_SIZE_MEDIUM, SCREEN_WIDTH // 2, 100, COLOR_WHITE, manager.pixel_font)
        
        if not hasattr(self, 'music_btn'):
            self.music_btn = ui.Button("Music: ON" if manager.settings.get("music") else "Music: OFF", SCREEN_WIDTH // 2, 180, 250, 50, (112, 128, 144), (160, 170, 180), manager.pixel_font, "click")
            self.sfx_btn = ui.Button("SFX: ON" if manager.settings.get("sfx") else "SFX: OFF", SCREEN_WIDTH // 2, 240, 250, 50, (112, 128, 144), (160, 170, 180), manager.pixel_font, "click")
            self.back_btn = ui.Button("Back", SCREEN_WIDTH // 2, 320, 150, 40, (180, 50, 50), (220, 80, 80), manager.small_font, "click")

        # Update button text
        self.music_btn.text = "Music: ON" if manager.settings.get("music") else "Music: OFF"
        self.sfx_btn.text = "SFX: ON" if manager.settings.get("sfx") else "SFX: OFF"
        
        self.music_btn.draw(manager.screen)
        self.sfx_btn.draw(manager.screen)
        self.back_btn.draw(manager.screen)

    def draw_leaderboard(self, manager):
        manager.screen.blit(manager.menu_overlay, (0, 0))
        ui.draw_text(manager.screen, "LEADERBOARD", FONT_SIZE_MEDIUM, SCREEN_WIDTH // 2, 100, COLOR_WHITE, manager.pixel_font)
        
        high_scores = assets.load_leaderboard()
        for i, entry in enumerate(high_scores[:5]):
            name = entry.get("name", "Unknown")
            score = entry.get("score", 0)
            ui.draw_text(manager.screen, f"{i+1}. {name}: {score}", FONT_SIZE_SMALL, SCREEN_WIDTH // 2, 160 + i * 30, COLOR_WHITE, manager.small_font)
        
        if not hasattr(self, 'back_btn'):
            self.back_btn = ui.Button("Back", SCREEN_WIDTH // 2, 320, 150, 40, (180, 50, 50), (220, 80, 80), manager.small_font, "click")
        
        self.back_btn.draw(manager.screen)
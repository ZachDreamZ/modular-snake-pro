import pygame
from config import *
import assets
import ui

class MenuState:
    def __init__(self):
        self.sub_state = "MENU"

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

    def draw(self, manager, offset_x, offset_y):
        if self.sub_state == "MENU":
            manager.screen.blit(manager.menu_overlay, (0, 0))
            manager.screen.blit(manager.title_surf, (SCREEN_WIDTH // 2 - manager.title_surf.get_width() // 2, 100))
            for btn in manager.menu_buttons:
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
        for i, (name, score) in enumerate(high_scores[:5]):
            ui.draw_text(manager.screen, f"{i+1}. {name}: {score}", FONT_SIZE_SMALL, SCREEN_WIDTH // 2, 160 + i * 30, COLOR_WHITE, manager.small_font)
        
        if not hasattr(self, 'back_btn'):
            self.back_btn = ui.Button("Back", SCREEN_WIDTH // 2, 320, 150, 40, (180, 50, 50), (220, 80, 80), manager.small_font, "click")
        
        self.back_btn.draw(manager.screen)
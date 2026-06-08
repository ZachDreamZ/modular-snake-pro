import pygame
from config import *
import game_assets
import ui
from localization_manager import loc
from analytics_manager import analytics

class ShopState:
    def __init__(self):
        pass

    def handle_events(self, manager, events):
        mx, my = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    manager.change_state("MENU")
                    return

            if event.type == pygame.MOUSEBUTTONDOWN:
                idx = manager.shop_ui.handle_click(mx, my, manager.theme_keys)
                if idx is not None:
                    theme_key = manager.theme_keys[idx]
                    manager.shop_index = idx

                    if theme_key in manager.unlocked_themes:
                        manager.theme = THEMES[theme_key]
                        game_assets.save_settings({"theme": theme_key})
                        analytics.log_theme_equip(theme_key)
                        manager.bg_surface = manager._generate_bg_surface()
                        manager.trigger_toast(loc.get_text("shop_equipped") + loc.get_text(f"theme_{theme_key}"))
                    else:
                        cost = manager.theme_costs.get(theme_key, 0)
                        req_ach = THEMES[theme_key].get("required_achievement")

                        if req_ach and req_ach not in manager.unlocked_achievements:
                            manager.trigger_toast(loc.get_text("shop_req_achievement") + req_ach)
                        elif manager.total_points >= cost:
                            manager.total_points -= cost
                            manager.unlocked_themes.append(theme_key)
                            manager.theme = THEMES[theme_key]
                            game_assets.save_total_points(manager.total_points)
                            game_assets.save_unlocked_themes(manager.unlocked_themes)
                            game_assets.save_settings({"theme": theme_key})
                            manager.bg_surface = manager._generate_bg_surface()
                            manager.trigger_toast(loc.get_text("shop_unlocked") + loc.get_text(f"theme_{theme_key}"))
                        else:
                            manager.trigger_toast(loc.get_text("shop_not_enough_pts"))

    def update(self, manager):
        pass

    def draw(self, manager, offset_x, offset_y):
        manager.shop_ui.draw(manager.screen, manager)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 60))
        manager.screen.blit(overlay, (0, 0))

        ui.draw_text(manager.screen, loc.get_text("shop_back_label"), FONT_SIZE_TINY, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30, COLOR_GREY, manager.small_font, font_multiplier=manager.settings.get("font_scale", 1.0), settings=manager.settings)

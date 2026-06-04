import pygame
from config import *
import assets
import ui

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
                        # Equip
                        manager.theme = THEMES[theme_key]
                        assets.save_settings({"theme": theme_key})
                    else:
                        # Attempt Purchase
                        cost = manager.theme_costs.get(theme_key, 0)
                        req_ach = THEMES[theme_key].get("required_achievement")
                        
                        if req_ach and req_ach not in manager.unlocked_achievements:
                            manager.trigger_toast(f"Achievement Required: {req_ach}")
                        elif manager.total_points >= cost:
                            manager.total_points -= cost
                            manager.unlocked_themes.append(theme_key)
                            manager.theme = THEMES[theme_key]
                            assets.save_total_points(manager.total_points)
                            assets.save_unlocked_themes(manager.unlocked_themes)
                            assets.save_settings({"theme": theme_key})
                            manager.trigger_toast(f"Unlocked {THEMES[theme_key]['name']}!")
                        else:
                            manager.trigger_toast("Not enough points!")

    def update(self, manager):
        pass

    def draw(self, manager, offset_x, offset_y):
        # Background is handled by manager
        manager.shop_ui.draw(manager.screen, manager)
        
        # Navigation Label
        ui.draw_text(manager.screen, "S: Back to Menu", FONT_SIZE_TINY, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20, COLOR_GREY, manager.small_font)
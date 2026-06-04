import pygame
import math
import random
from config import *
import assets
from entities import Snake

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, font, hover_sound=None):
        self.text = text
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.hover_sound = hover_sound
        self.is_hovered = False
        self.is_pressed = False
        
        # Cache text surface
        self.text_surf = self.font.render(self.text, True, (255, 255, 255))

    def update(self, mouse_pos, mouse_buttons=(False, False, False)):
        if self.rect.collidepoint(mouse_pos):
            if not self.is_hovered:
                if self.hover_sound:
                    assets.sound_manager.play(self.hover_sound)
                self.is_hovered = True
            
            if mouse_buttons[0]: # Left click
                self.is_pressed = True
            else:
                self.is_pressed = False
        else:
            self.is_hovered = False
            self.is_pressed = False

    def draw(self, surface):
        # Determine visual state
        if self.is_pressed:
            draw_rect = self.rect.inflate(-6, -6)
            color = [max(0, c - 30) for c in self.hover_color] # Darken hover color
        elif self.is_hovered:
            draw_rect = self.rect.inflate(8, 8)
            color = self.hover_color
        else:
            draw_rect = self.rect
            color = self.color
        
        # Draw outer glow if hovered and not pressed
        if self.is_hovered and not self.is_pressed:
            glow_rect = draw_rect.inflate(6, 6)
            # Draw a soft glow using a slightly lighter version of the color
            glow_color = [min(255, c + 40) for c in color]
            pygame.draw.rect(surface, glow_color, glow_rect, 2, border_radius=14)
        
        # Draw button body with rounded corners
        pygame.draw.rect(surface, color, draw_rect, border_radius=12)
        pygame.draw.rect(surface, (0, 0, 0), draw_rect, 3, border_radius=12)
        
        # Draw cached text
        text_rect = self.text_surf.get_rect(center=draw_rect.center)
        surface.blit(self.text_surf, text_rect)

        # Sleek animated cursor marker next to the highlighted button text
        if self.is_hovered and not self.is_pressed:
            t = pygame.time.get_ticks() / 150
            offset = math.sin(t) * 4
            marker_rect = pygame.Rect(draw_rect.left + 12, draw_rect.top + 10 + offset, 5, draw_rect.height - 20)
            pygame.draw.rect(surface, (255, 255, 255), marker_rect, border_radius=2)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

def draw_text(surface, text, size, x, y, color, font=None):
    if font is None:
        font = pygame.font.SysFont("Arial", size, bold=True)
    
    shadow_surf = font.render(text, True, (0, 0, 0))
    shadow_rect = shadow_surf.get_rect(center=(x + 2, y + 2))
    surface.blit(shadow_surf, shadow_rect)
    
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(x, y))
    surface.blit(text_surf, text_rect)

def draw_panel(surface, x, y, w, h, alpha=150):
    panel = pygame.Surface((w, h), pygame.SRCALPHA)
    panel.fill((0, 0, 0, alpha))
    surface.blit(panel, (x, y))

def draw_overlay(surface, title, subtitle, title_font=None, sub_font=None):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    surface.blit(overlay, (0, 0))
    
    draw_text(surface, title, FONT_SIZE_HUGE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3, COLOR_WHITE, font=title_font)
    draw_text(surface, subtitle, FONT_SIZE_MEDIUM, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, COLOR_WHITE, font=sub_font)

def get_text_rect(text, size, x, y):
    font = pygame.font.SysFont("Arial", size, bold=True)
    text_surf = font.render(text, True, (0,0,0))
    return text_surf.get_rect(center=(x, y))

class ShopUI:
    def __init__(self):
        # Adjusted defaults to provide extra padding and spacing to avoid clipping on reskinned UI
        self.grid_start_x = 400
        self.grid_start_y = 120
        self.card_w = 140
        self.card_h = 90
        # Horizontal / vertical spacing between cards
        self.h_spacing = 30
        self.v_spacing = 20
        self.pedestal_x = 200
        self.pedestal_y = 220

    def draw(self, surface, manager):
        # Preview Pedestal
        px, py = self.pedestal_x, self.pedestal_y
        
        # Subtle particle sparks behind the pedestal
        t = pygame.time.get_ticks() / 1000
        for i in range(8):
            angle = (t * 0.5) + (i * (math.pi * 2 / 8))
            sx = px + math.cos(angle) * 70
            sy = py + math.sin(angle) * 30 - 20
            spark_size = random.randint(2, 4)
            pygame.draw.circle(surface, (255, 255, 200), (int(sx), int(sy)), spark_size)

        pygame.draw.ellipse(surface, (40, 40, 40), (px-80, py, 160, 60))
        pygame.draw.ellipse(surface, (60, 60, 60), (px-60, py-10, 120, 40))
        
        # Animated Preview Snake
        preview_theme = THEMES[manager.theme_keys[manager.shop_index]]
        preview_snake = Snake((px, py), preview_theme["snake_color"], preview_theme["snake_color_dark"])
        t = pygame.time.get_ticks() / 500
        preview_snake.body = [(px + math.cos(t+i*0.3)*30, py + math.sin(t+i*0.3)*20) for i in range(5)]
        preview_snake.draw(surface)
        draw_text(surface, "PREVIEW", FONT_SIZE_SMALL, px, py + 70, COLOR_GREY)

        # Skin Grid
        for i, theme_key in enumerate(manager.theme_keys):
            col = i % 2
            row = i // 2
            cx = self.grid_start_x + col * (self.card_w + self.h_spacing)
            cy = self.grid_start_y + row * (self.card_h + self.v_spacing)
            rect = pygame.Rect(cx, cy, self.card_w, self.card_h)
            
            rarity = THEMES[theme_key].get("rarity", "common")
            border_color = COLOR_RARITY_COMMON if rarity == "common" else COLOR_RARITY_EPIC if rarity == "epic" else COLOR_RARITY_LEGENDARY
            
            bg_color = (60, 60, 60) if i == manager.shop_index else (30, 30, 30)
            pygame.draw.rect(surface, bg_color, rect, border_radius=10)
            pygame.draw.rect(surface, border_color, rect, 3, border_radius=10)
            
            draw_text(surface, THEMES[theme_key]["name"], FONT_SIZE_SMALL, cx + self.card_w // 2, cy + 25, COLOR_WHITE)
            
            is_unlocked = theme_key in manager.unlocked_themes
            is_equipped = manager.theme == THEMES[theme_key]
            req_ach = THEMES[theme_key].get("required_achievement")
            
            btn_text = "Equipped" if is_equipped else ("Equip" if is_unlocked else f"{manager.theme_costs[theme_key]} pts")
            btn_color = COLOR_GREEN if is_unlocked and not is_equipped else COLOR_GREY if is_equipped else COLOR_YELLOW
            if req_ach and req_ach not in manager.unlocked_achievements:
                btn_text = "🔒 Locked"
                btn_color = (50, 50, 50)

            btn_rect = pygame.Rect(cx + 15, cy + 35, self.card_w - 30, 25)
            pygame.draw.rect(surface, btn_color, btn_rect, border_radius=5)
            draw_text(surface, btn_text, 10, btn_rect.centerx, btn_rect.centery, COLOR_BLACK)

    def get_card_at_pos(self, mouse_pos, manager):
        mx, my = mouse_pos
        for i, theme_key in enumerate(manager.theme_keys):
            col = i % 2
            row = i // 2
            cx = self.grid_start_x + col * (self.card_w + self.h_spacing)
            cy = self.grid_start_y + row * (self.card_h + self.v_spacing)
            rect = pygame.Rect(cx, cy, self.card_w, self.card_h)
            if rect.collidepoint(mx, my):
                return i
        return None

    def handle_click(self, mx, my, theme_keys):
        for i, theme_key in enumerate(theme_keys):
            col = i % 2
            row = i // 2
            cx = self.grid_start_x + col * (self.card_w + self.h_spacing)
            cy = self.grid_start_y + row * (self.card_h + self.v_spacing)
            rect = pygame.Rect(cx, cy, self.card_w, self.card_h)
            if rect.collidepoint(mx, my):
                return i
        return None

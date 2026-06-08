import pygame
import math
import random
from config import *
import game_assets
from entities import Snake
from localization_manager import loc

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, font, hover_sound=None, key=None):
        self.text = text
        self.key = key
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.hover_sound = hover_sound
        self.is_hovered = False
        self.is_pressed = False
        self.text_surf = self.font.render(self.text, True, (255, 255, 255))

    def update(self, mouse_pos, mouse_buttons=(False, False, False)):
        if self.rect.collidepoint(mouse_pos):
            if not self.is_hovered:
                if self.hover_sound:
                    game_assets.sound_manager.play(self.hover_sound)
                self.is_hovered = True
            if mouse_buttons[0]:
                self.is_pressed = True
            else:
                self.is_pressed = False
        else:
            self.is_hovered = False
            self.is_pressed = False

    def draw(self, surface):
        if self.is_pressed:
            draw_rect = self.rect.inflate(-6, -6)
            color = [max(0, c - 30) for c in self.hover_color]
        elif self.is_hovered:
            draw_rect = self.rect.inflate(8, 8)
            color = self.hover_color
        else:
            draw_rect = self.rect
            color = self.color

        if self.is_hovered and not self.is_pressed:
            glow_rect = draw_rect.inflate(6, 6)
            glow_color = [min(255, c + 40) for c in color]
            pygame.draw.rect(surface, glow_color, glow_rect, 2, border_radius=14)

        pygame.draw.rect(surface, color, draw_rect, border_radius=12)
        pygame.draw.rect(surface, (0, 0, 0), draw_rect, 2, border_radius=12)

        text_rect = self.text_surf.get_rect(center=draw_rect.center)
        surface.blit(self.text_surf, text_rect)

        if self.is_hovered and not self.is_pressed:
            t = pygame.time.get_ticks() / 150
            offset = math.sin(t) * 4
            marker_rect = pygame.Rect(draw_rect.left + 12, draw_rect.top + 10 + offset, 5, draw_rect.height - 20)
            pygame.draw.rect(surface, (255, 255, 255), marker_rect, border_radius=2)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

_font_cache = {}

def resolve_color(color, settings=None):
    if not settings:
        return color
    mode = settings.get("colorblind", "none")
    if mode == "none":
        return color
    from config import COLORBLIND_PALETTES
    palette = COLORBLIND_PALETTES.get(mode, COLORBLIND_PALETTES["none"])
    color_map = {
        (0, 255, 0): palette["green"],
        (255, 0, 0): palette["red"],
        (255, 255, 0): palette["yellow"],
        (128, 0, 128): palette["purple"],
        (0, 0, 255): palette["blue"],
    }
    return color_map.get(color, color)

def draw_text(surface, text, size, x, y, color, font=None, font_multiplier=1.0, settings=None):
    adjusted_size = int(size * font_multiplier)
    if font is None:
        key = (adjusted_size, "Arial", True)
        if key not in _font_cache:
            _font_cache[key] = pygame.font.SysFont("Arial", adjusted_size, bold=True)
        font = _font_cache[key]
    resolved_color = resolve_color(color[:3] if isinstance(color, tuple) and len(color) >= 3 else color, settings)
    text_surf = font.render(text, True, resolved_color)
    if isinstance(color, tuple) and len(color) == 4:
        text_surf.set_alpha(color[3])
    text_rect = text_surf.get_rect(center=(x, y))
    surface.blit(text_surf, text_rect)

def draw_glow_text(surface, text, size, x, y, color, font=None):
    draw_text(surface, text, size, x + 2, y + 2, (0, 0, 0), font=font)
    for r in range(3, 0, -1):
        gc = tuple(min(255, c + 50) for c in color[:3])
        draw_text(surface, text, size, x, y, gc, font=font)
    draw_text(surface, text, size, x, y, color, font=font)

def draw_panel(surface, x, y, w, h, alpha=150, border_color=None):
    panel = pygame.Surface((w, h), pygame.SRCALPHA)
    panel.fill((0, 0, 0, alpha))
    # Rounded corners via overlay
    pygame.draw.rect(panel, (0, 0, 0, 0), panel.get_rect(), border_radius=8)
    surface.blit(panel, (x, y))
    if border_color:
        pygame.draw.rect(surface, border_color, (x, y, w, h), 2, border_radius=8)

def draw_overlay(surface, title, subtitle, title_font=None, sub_font=None):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    surface.blit(overlay, (0, 0))
    draw_glow_text(surface, title, FONT_SIZE_HUGE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3, (255, 200, 50), font=title_font)
    draw_text(surface, subtitle, FONT_SIZE_MEDIUM, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, COLOR_WHITE, font=sub_font)

def get_text_rect(text, size, x, y):
    font = pygame.font.SysFont("Arial", size, bold=True)
    text_surf = font.render(text, True, (0,0,0))
    return text_surf.get_rect(center=(x, y))

class ShopUI:
    def __init__(self):
        self.grid_start_x = 400
        self.grid_start_y = 120
        self.card_w = 140
        self.card_h = 80
        self.h_spacing = 30
        self.v_spacing = 10
        self.pedestal_x = 200
        self.pedestal_y = 220

    def draw(self, surface, manager):
        px, py = self.pedestal_x, self.pedestal_y

        t = pygame.time.get_ticks() / 1000
        for i in range(12):
            angle = (t * 0.5) + (i * (math.pi * 2 / 12))
            sx = px + math.cos(angle) * 80
            sy = py + math.sin(angle) * 35 - 15
            spark_size = random.randint(2, 5)
            spark_color = (255, random.randint(200, 255), 150)
            pygame.draw.circle(surface, spark_color, (int(sx), int(sy)), spark_size)

        # Pedestal glow
        for r in range(20, 0, -2):
            alpha = max(0, 60 - r * 2)
            glow_surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            gc = (60, 60, 60, alpha)
            pygame.draw.ellipse(glow_surf, gc, glow_surf.get_rect())
            surface.blit(glow_surf, (px - r, py + 60 - r // 2))

        pygame.draw.ellipse(surface, (50, 50, 50), (px-80, py, 160, 60))
        pygame.draw.ellipse(surface, (70, 70, 70), (px-60, py-10, 120, 40))

        preview_theme = THEMES[manager.theme_keys[manager.shop_index]]
        preview_snake = Snake((px, py), preview_theme["snake_color"], preview_theme["snake_color_dark"])
        t = pygame.time.get_ticks() / 500
        preview_snake.body = [(px + math.cos(t+i*0.3)*30, py + math.sin(t+i*0.3)*20) for i in range(5)]
        preview_snake.draw(surface)
        draw_text(surface, loc.get_text("shop_preview"), FONT_SIZE_SMALL, px, py + 80, COLOR_GREY, font_multiplier=manager.settings.get("font_scale", 1.0), settings=manager.settings)

        for i, theme_key in enumerate(manager.theme_keys):
            col = i % 2
            row = i // 2
            cx = self.grid_start_x + col * (self.card_w + self.h_spacing)
            cy = self.grid_start_y + row * (self.card_h + self.v_spacing)
            rect = pygame.Rect(cx, cy, self.card_w, self.card_h)

            rarity = THEMES[theme_key].get("rarity", "common")
            border_color = COLOR_RARITY_COMMON if rarity == "common" else COLOR_RARITY_EPIC if rarity == "epic" else COLOR_RARITY_LEGENDARY

            bg_color = (60, 60, 60) if i == manager.shop_index else (30, 30, 30)
            shadow_rect = rect.copy()
            shadow_rect.y += 3
            pygame.draw.rect(surface, (0, 0, 0, 60), shadow_rect, border_radius=10)
            pygame.draw.rect(surface, bg_color, rect, border_radius=10)
            pygame.draw.rect(surface, border_color, rect, 2, border_radius=10)

            if i == manager.shop_index:
                glow_rect = rect.inflate(4, 4)
                glow_color = list(border_color) + [80]
                pygame.draw.rect(surface, glow_color, glow_rect, 3, border_radius=12)

            draw_text(surface, loc.get_text(f"theme_{theme_key}"), FONT_SIZE_SMALL, cx + self.card_w // 2, cy + 25, COLOR_WHITE, font_multiplier=manager.settings.get("font_scale", 1.0), settings=manager.settings)

            is_unlocked = theme_key in manager.unlocked_themes
            is_equipped = manager.theme == THEMES[theme_key]
            req_ach = THEMES[theme_key].get("required_achievement")

            btn_text = "Equipped" if is_equipped else ("Equip" if is_unlocked else f"{manager.theme_costs[theme_key]} pts")
            btn_color = COLOR_GREEN if is_unlocked and not is_equipped else COLOR_GREY if is_equipped else COLOR_YELLOW
            if req_ach and req_ach not in manager.unlocked_achievements:
                btn_text = "Locked"
                btn_color = (50, 50, 50)

            btn_rect = pygame.Rect(cx + 15, cy + 30, self.card_w - 30, 22)
            pygame.draw.rect(surface, btn_color, btn_rect, border_radius=5)
            draw_text(surface, btn_text, 10, btn_rect.centerx, btn_rect.centery, COLOR_BLACK, font_multiplier=manager.settings.get("font_scale", 1.0), settings=manager.settings)

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

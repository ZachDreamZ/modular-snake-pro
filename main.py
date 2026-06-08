import pygame
import game_assets
from config import *
from states.state_manager import StateManager
from analytics_manager import analytics

SPLASH_DURATION = 90

def _show_splash(screen, clock):
    try:
        splash_font_lg = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 36)
        splash_font_sm = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 14)
    except Exception:
        splash_font_lg = pygame.font.SysFont("Arial", 36, bold=True)
        splash_font_sm = pygame.font.SysFont("Arial", 14, bold=True)

    # Pre-render
    glow_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            c = (20, 60, 20) if (x // BLOCK_SIZE + y // BLOCK_SIZE) % 2 == 0 else (10, 30, 10)
            pygame.draw.rect(glow_surf, c, (x, y, BLOCK_SIZE, BLOCK_SIZE))

    for frame in range(SPLASH_DURATION):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return True

        screen.blit(glow_surf, (0, 0))

        alpha = min(255, frame * 6) if frame < 40 else (255 if frame < SPLASH_DURATION - 30 else max(0, 255 - (frame - (SPLASH_DURATION - 30)) * 10))

        title_text = splash_font_lg.render("SNAKE GRADIENT", True, (0, 255, 0))
        title_text.set_alpha(alpha)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        screen.blit(title_text, title_rect)

        sub_text = splash_font_sm.render("AI Challenge", True, (100, 255, 100))
        sub_text.set_alpha(alpha)
        sub_rect = sub_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(sub_text, sub_rect)

        ver_text = splash_font_sm.render(f"v{VERSION}", True, (128, 128, 128))
        ver_text.set_alpha(alpha)
        ver_rect = ver_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 55))
        screen.blit(ver_text, ver_rect)

        hint_text = splash_font_sm.render("Press any key to skip", True, (64, 64, 64))
        hint_text.set_alpha(min(255, frame * 4))
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        screen.blit(hint_text, hint_rect)

        pygame.display.flip()
        clock.tick(60)

    return True

def main():
    analytics.log_session_start()
    game_assets.download_assets()

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Gradient - AI Challenge")
    try:
        icon = pygame.image.load("assets/icon.png")
        pygame.display.set_icon(icon)
    except Exception:
        pass

    clock = pygame.time.Clock()

    if not _show_splash(screen, clock):
        pygame.quit()
        return

    manager = StateManager(screen, clock)

    running = True
    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        manager.handle_events(events)
        manager.update()
        manager.draw()

        pygame.display.flip()

        if manager.state == "PLAYING":
            clock.tick(manager.game_speed)
        else:
            clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

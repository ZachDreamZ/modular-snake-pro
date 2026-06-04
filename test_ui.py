import pygame
import sys
from states.state_manager import StateManager
from config import SCREEN_WIDTH, SCREEN_HEIGHT

def simulate_click(manager, x, y):
    print(f"Simulating click at ({x}, {y})")
    # Create a MOUSEBUTTONDOWN event
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (x, y)})
    # We also need to set the mouse position for any logic that uses pygame.mouse.get_pos()
    pygame.mouse.set_pos((x, y))
    manager.handle_events([event])

def simulate_key(manager, key):
    print(f"Simulating key press: {key}")
    event = pygame.event.Event(pygame.KEYDOWN, {'key': key})
    manager.handle_events([event])

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("UI Audit Tool")
    clock = pygame.time.Clock()
    
    manager = StateManager(screen, clock)
    
    # 1. Capture Main Menu
    print("Capturing Main Menu...")
    manager.update()
    manager.draw()
    pygame.display.flip()
    pygame.image.save(screen, "audit_main_menu.png")
    print("Saved audit_main_menu.png")
    
    # 2. Go to Shop
    # SHOP button is at (300, 260)
    simulate_click(manager, 300, 260)
    
    # Update a few times to ensure state transition and animations
    for _ in range(10):
        manager.update()
        manager.draw()
        pygame.display.flip()
    
    print("Capturing Skin Shop...")
    pygame.image.save(screen, "audit_skin_shop.png")
    print("Saved audit_skin_shop.png")
    
    # 3. Return to Menu
    # Shop uses 'S' key to go back
    simulate_key(manager, pygame.K_s)
    
    for _ in range(10):
        manager.update()
        manager.draw()
        pygame.display.flip()
        
    print("Capturing Return to Menu...")
    pygame.image.save(screen, "audit_return_menu.png")
    print("Saved audit_return_menu.png")
    
    pygame.quit()
    print("Audit complete.")

if __name__ == "__main__":
    main()
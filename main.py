import pygame
import assets
from config import *
from states import StateManager

def main():
    # Automatically download required game assets
    assets.download_assets()

    # Initialize Pygame
    pygame.init()
    
    # Setup the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Gradient - AI Challenge")
    
    # Setup the clock for frame rate control
    clock = pygame.time.Clock()
    
    # Initialize the state manager
    manager = StateManager(screen, clock)
    
    running = True
    while running:
        # Get all events from the queue
        events = pygame.event.get()
        
        # Handle system-level events (like closing the window)
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        # Delegate event handling to the state manager
        manager.handle_events(events)
        
        # Update game logic
        manager.update()
        
        # Render the current state
        manager.draw()
        
        # Update the display
        pygame.display.flip()
        
        # Control the game speed
        if manager.state == "PLAYING":
            # Use the dynamic game speed for gameplay
            clock.tick(manager.game_speed)
        else:
            # Use a constant smooth frame rate for menus/UI
            clock.tick(60)

    # Clean up and exit
    pygame.quit()

if __name__ == "__main__":
    main()
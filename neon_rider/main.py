# main.py - Entry point for Neon Rider

import pygame
import sys
from settings import *
from game_manager import GameManager

def main():
    """Main game loop."""
    pygame.init()
    surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    
    game_manager = GameManager(surface)
    
    running = True
    while running:
        # Handle input
        events = pygame.event.get()
        result = game_manager.handle_input(events)
        if result is False:
            running = False
        else:
            _, torque_input = result
        
        # Update
        game_manager.update()
        
        # Render
        game_manager.render()
        
        # Cap framerate
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

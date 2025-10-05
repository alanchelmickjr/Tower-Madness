"""
Tower Madness / Elevator Operator
Main game entry point for SF Tech Week Algorave
Arcade cabinet ready with 2-player support
"""

import pygame
import sys
from game.core.engine import GameEngine
from game.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FPS

def main():
    """Main entry point for Tower Madness game."""
    pygame.init()
    pygame.mixer.init()
    
    # Set up display for arcade cabinet
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    
    # Create game engine
    engine = GameEngine(screen, clock)
    
    # Main game loop
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
        
        # Handle events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Update and draw
        engine.update(dt, events)
        engine.draw()
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
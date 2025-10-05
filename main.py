"""
Tower Madness / Elevator Operator
Main game entry point for SF Tech Week Algorave
Web-compatible with Pygbag async support
"""

import pygame
import sys
import asyncio
from game.core.engine import GameEngine
from game.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FPS

async def main():
    """Async main entry point for web deployment with Pygbag."""
    print("Tower Madness starting...")
    
    pygame.init()
    pygame.mixer.init()
    
    # Set up display for arcade cabinet
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    
    print(f"Display initialized: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    
    # Create game engine
    engine = GameEngine(screen, clock)
    print("Game engine created, starting main loop...")
    
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
        
        # Yield control for web browser - this is critical for Pygbag
        await asyncio.sleep(0)
    
    pygame.quit()
    print("Tower Madness ended")

# Entry point for Pygbag
if __name__ == "__main__":
    asyncio.run(main())
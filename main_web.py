#!/usr/bin/env python3
"""
Web-compatible main entry point for Tower Madness / Elevator Operator
Uses async/await for Pygbag compatibility
"""

import asyncio
import pygame
import sys
from game.core.engine import GameEngine

async def main():
    """Async main game loop for web compatibility."""
    print("Tower Madness starting (web version)...")
    
    pygame.init()
    pygame.mixer.init()
    
    # Set up display - CRITICAL for pybag!
    from game.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FPS
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    
    print(f"Display initialized: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    
    # Create game engine with required parameters
    engine = GameEngine(screen, clock)
    print("Game engine created, starting main loop...")
    
    # Game loop
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
                
        # Update game
        engine.update(dt, events)
        
        # Draw game
        engine.draw()
        
        # Update display
        pygame.display.flip()
        
        # Yield control for web browser - critical for Pygbag
        await asyncio.sleep(0)
    
    pygame.quit()
    print("Tower Madness ended")

# For Pygbag - it looks for asyncio.run
if __name__ == "__main__":
    asyncio.run(main())
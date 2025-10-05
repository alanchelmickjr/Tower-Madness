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
    pygame.init()
    
    # Create game engine
    engine = GameEngine()
    
    # Game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        dt = clock.tick(60) / 1000.0  # 60 FPS
        
        # Handle events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                
        # Update game
        engine.update(dt, events)
        
        # Draw game
        engine.draw()
        
        # Update display
        pygame.display.flip()
        
        # Yield control for web browser
        await asyncio.sleep(0)
    
    pygame.quit()

# For Pygbag - it looks for asyncio.run
if __name__ == "__main__":
    asyncio.run(main())
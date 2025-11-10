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
    try:
        print("🏢 Tower Madness starting (web version)...")
        print("1. Initializing pygame...")

        # Initialize pygame
        pygame.init()

        # Initialize audio with error handling for web
        print("2. Initializing audio...")
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            print("   ✅ Audio initialized")
        except Exception as e:
            print(f"   ⚠️  Audio initialization failed: {e}")
            print("   ⚠️  Continuing without audio...")

        # Set up display - CRITICAL for pygbag!
        print("3. Setting up display...")
        from game.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FPS
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        clock = pygame.time.Clock()

        print(f"   ✅ Display initialized: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")

        # Create game engine with required parameters
        print("4. Creating game engine...")
        engine = GameEngine(screen, clock)
        print("   ✅ Game engine created")

        print("5. Starting main game loop...")
        print("=" * 50)

        # Game loop
        running = True
        frame_count = 0

        while running:
            dt = clock.tick(FPS) / 1000.0  # Delta time in seconds

            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Don't quit on first ESC, let game handle it
                        pass

            # Update game
            try:
                engine.update(dt, events)
            except Exception as e:
                print(f"❌ Error in engine.update(): {e}")
                import traceback
                traceback.print_exc()

            # Draw game
            try:
                engine.draw()
            except Exception as e:
                print(f"❌ Error in engine.draw(): {e}")
                import traceback
                traceback.print_exc()

            # Update display
            pygame.display.flip()

            # Debug output for first few frames
            frame_count += 1
            if frame_count <= 3:
                print(f"   Frame {frame_count} rendered successfully")
            elif frame_count == 4:
                print("   ✅ Frame rendering working normally...")

            # Yield control for web browser - critical for Pygbag
            await asyncio.sleep(0)

        pygame.quit()
        print("=" * 50)
        print("Tower Madness ended normally")

    except Exception as e:
        print("=" * 50)
        print(f"❌ CRITICAL ERROR in main(): {e}")
        import traceback
        traceback.print_exc()
        print("=" * 50)
        raise

# For Pygbag - it looks for asyncio.run
if __name__ == "__main__":
    asyncio.run(main())
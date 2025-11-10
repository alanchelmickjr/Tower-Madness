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
    print("="*60)
    print("🎮 TOWER MADNESS - ELEVATOR OPERATOR 🎮")
    print("="*60)
    print("Starting initialization...")

    try:
        # Initialize Pygame
        print("1. Initializing pygame...")
        pygame.init()
        print("   ✓ Pygame initialized")

        # Initialize audio
        print("2. Initializing pygame.mixer...")
        try:
            pygame.mixer.init()
            mixer_info = pygame.mixer.get_init()
            if mixer_info:
                print(f"   ✓ Audio initialized: {mixer_info}")
            else:
                print("   ⚠ Audio initialized but mixer returned None")
        except Exception as e:
            print(f"   ✗ Audio initialization error: {e}")
            print("   ℹ Game will continue without sound")

        # Set up display
        print(f"3. Creating display ({SCREEN_WIDTH}x{SCREEN_HEIGHT})...")
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        clock = pygame.time.Clock()
        print("   ✓ Display created successfully")

        # Create game engine
        print("4. Creating game engine...")
        engine = GameEngine(screen, clock)
        print("   ✓ Game engine created")

        print("="*60)
        print("🚀 INITIALIZATION COMPLETE - Starting main loop...")
        print("="*60)

    except Exception as e:
        print(f"CRITICAL ERROR during initialization: {e}")
        import traceback
        traceback.print_exc()
        raise

    # Main game loop
    running = True
    frame_count = 0
    while running:
        try:
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

            # Log first few frames for debugging
            frame_count += 1
            if frame_count <= 5:
                print(f"Frame {frame_count} rendered successfully")
            elif frame_count == 6:
                print("Frame rendering working normally...")

            # Yield control for web browser - this is critical for Pygbag
            await asyncio.sleep(0)

        except Exception as e:
            print(f"ERROR in main loop (frame {frame_count}): {e}")
            import traceback
            traceback.print_exc()
            # Continue running to show error on screen if engine can still draw
            # If errors persist, user can press ESC to exit

    print("="*60)
    print("Shutting down Tower Madness...")
    pygame.quit()
    print("Tower Madness ended cleanly")
    print("="*60)

# Entry point for Pygbag
if __name__ == "__main__":
    asyncio.run(main())
# Copilot Instructions for Tower Madness

## Project Overview
- Tower Madness is a retro elevator game built with Pygame, designed for standup consoles and mobile devices.
- The game features 16 floors, with sprite-based passengers and NPCs entering and exiting the elevator.
- Inspiration: Classic elevator operator games. See https://frontiertower.io for thematic details.

## Architecture & Key Components
- Main game loop: Handles rendering, input, and game state updates.
- Elevator system: Manages elevator movement, floor logic, and passenger/NPC interactions.
- Sprite management: Uses Pygame sprites for elevator, passengers, NPCs, and UI elements.
- Event system: Triggers for floor arrivals, passenger actions, and game events.
- Levels: 16 distinct floors, each with unique challenges or NPC behaviors.

## Developer Workflows
- **Run Game:**
  - `python main.py` (or equivalent entry point)
- **Build Assets:**
  - Place sprites and sound files in `/assets` or similar directory.
- **Testing:**
  - Manual playtesting is primary; add automated tests in `/tests` if present.
- **Debugging:**
  - Use Pygame's built-in event logging and print statements for debugging.

## Project-Specific Conventions
- Sprite filenames should be descriptive (e.g., `npc_oldlady.png`, `passenger_kid.png`).
- Floors are indexed 1-16; use constants for floor numbers.
- Game logic is separated from rendering code for maintainability.
- NPC and passenger behaviors are modular (e.g., separate classes or functions).

## Integration Points
- External assets: Sprites, sounds, and music loaded from `/assets`.
- Cross-component communication via event queues or signals (Pygame events).

## Example Patterns
- Elevator movement:
  ```python
  elevator.move_to_floor(target_floor)
  ```
- Passenger/NPC entry:
  ```python
  elevator.add_passenger(Passenger(...))
  ```
- Event handling:
  ```python
  for event in pygame.event.get():
      handle_event(event)
  ```

## Key Files & Directories
- `main.py`: Game entry point
- `/assets`: Sprites, sounds, music
- `/levels`: Floor definitions and logic
- `/npc`: NPC behavior modules
- `/tests`: Automated tests (if present)

---
Update this file as the codebase evolves. Reference this document for AI agent onboarding and productivity.

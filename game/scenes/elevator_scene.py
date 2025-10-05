"""
Main elevator gameplay scene for Tower Madness / Elevator Operator
Where the player operates the elevator between good and evil
"""

import pygame
import random
from game.core.constants import *
from game.entities.elevator import Elevator
from game.entities.floor import Floor
from game.entities.npc import NPC, GoodRobot, EvilRobot

class ElevatorScene:
    """Main gameplay scene managing elevator operations."""
    
    def __init__(self, player_count=1):
        """Initialize the elevator scene.
        
        Args:
            player_count: Number of players (1 or 2)
        """
        self.player_count = player_count
        
        # Create elevator starting at floor 0 (street level)
        elevator_x = SHAFT_X + (SHAFT_WIDTH - ELEVATOR_WIDTH) // 2
        elevator_y = SCREEN_HEIGHT - 250  # Start at ground floor
        self.elevator = Elevator(elevator_x, elevator_y)
        self.elevator.current_floor = 0  # Explicitly set starting floor
        
        # Create floors with proper positioning
        self.floors = {}
        base_y = SCREEN_HEIGHT - 200  # Base position for floor 0
        for floor_num in FLOORS.keys():
            # Account for missing floor 13
            adjusted_floor = floor_num
            if floor_num > 13:
                adjusted_floor = floor_num - 1  # Shift down by 1 to account for missing floor 13
            
            # Calculate y position (negative floors go down, positive go up)
            y_pos = base_y - (adjusted_floor * FLOOR_HEIGHT)
            self.floors[floor_num] = Floor(floor_num, y_pos)
            
        # NPCs
        self.npcs = []
        self.spawn_timer = 2.0  # Start spawning after 2 seconds
        self.spawn_interval = NPC_SPAWN_RATE
        
        # Game state
        self.score = 0
        self.passengers_delivered = 0
        self.chaos_level = 0  # Increases with evil robot activity
        self.harmony_level = 0  # Increases with good robot activity
        
        # Special characters
        self.john_the_doorman = None
        self.spawn_john_timer = 5.0  # John appears after 5 seconds
        self.alan_the_mastermind = None
        self.spawn_alan_timer = 10.0  # Alan appears after 10 seconds
        self.escaped_bad_robots = []  # Track bad robots escaping from basement
        
        # Visual effects
        self.screen_shake = 0
        self.flash_timer = 0
        self.flash_color = None
        
        # Tutorial/hints
        self.show_tutorial = True
        self.tutorial_timer = 10.0
        
        # Camera system for scrolling
        self.camera_y = 0
        self.camera_target_y = 0
        
    def update(self, dt, events):
        """Update the scene.
        
        Args:
            dt: Delta time in seconds
            events: List of pygame events
        """
        # Handle input
        self._handle_input(events)
        
        # Update elevator
        self.elevator.update(dt)
        
        # Update floors
        for floor in self.floors.values():
            floor.update(dt)
            
        # Update NPCs
        self._update_npcs(dt)
        
        # Spawn new NPCs
        self._spawn_npcs(dt)
        
        # Check for special NPCs
        self._update_john(dt)
        self._update_alan(dt)
        self._update_escaped_robots(dt)
        
        # Handle elevator arrivals
        self._handle_elevator_arrivals()
        
        # Update game balance
        self._update_game_balance(dt)
        
        # Update visual effects
        if self.screen_shake > 0:
            self.screen_shake = max(0, self.screen_shake - dt * 10)
        if self.flash_timer > 0:
            self.flash_timer = max(0, self.flash_timer - dt * 2)
            
        # Update camera to follow elevator
        self._update_camera(dt)
            
        # Update tutorial
        if self.show_tutorial:
            self.tutorial_timer -= dt
            if self.tutorial_timer <= 0:
                self.show_tutorial = False
                
    def _update_camera(self, dt):
        """Update camera to follow elevator."""
        # Calculate target camera position based on elevator
        elevator_screen_y = self.elevator.y - self.camera_y
        
        # Keep elevator centered in view for better visibility
        if self.elevator.current_floor > 1:
            # Start scrolling when above floor 1
            # Center the elevator in the screen
            target_offset = SCREEN_HEIGHT // 2 - self.elevator.y
            self.camera_target_y = target_offset
        elif self.elevator.current_floor < 0:
            # Scroll down for basement
            target_offset = SCREEN_HEIGHT - 300 - self.elevator.y
            self.camera_target_y = target_offset
        else:
            # Keep camera at ground level for floors 0-1
            self.camera_target_y = 0
            
        # Smooth camera movement with better tracking
        camera_diff = self.camera_target_y - self.camera_y
        # Faster camera movement for better responsiveness
        self.camera_y += camera_diff * dt * 8
                
    def _handle_input(self, events):
        """Handle player input."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Debug output
                print(f"Key pressed: {pygame.key.name(event.key)}")
                
                # Player 1 controls
                if event.key == PLAYER1_CONTROLS["up"]:
                    self._move_elevator_up()
                elif event.key == PLAYER1_CONTROLS["down"]:
                    self._move_elevator_down()
                elif event.key == PLAYER1_CONTROLS["open_doors"]:
                    print(f"Toggling doors. Current state: {self.elevator.doors_open}")
                    self.elevator.toggle_doors()
                    
                # Player 2 controls (if 2-player mode)
                if self.player_count == 2:
                    if event.key == PLAYER2_CONTROLS["up"]:
                        self._move_elevator_up()
                    elif event.key == PLAYER2_CONTROLS["down"]:
                        self._move_elevator_down()
                    elif event.key == PLAYER2_CONTROLS["open_doors"]:
                        self.elevator.toggle_doors()
                        
    def _move_elevator_up(self):
        """Move elevator up one floor."""
        current = self.elevator.current_floor
        # Check if we're at the roof (floor 17)
        if current >= 17:
            print(f"Can't go up - already at roof (Floor {current})")
        elif current == 12:
            # Skip floor 13 (doesn't exist)
            print(f"Moving up from floor {current} to floor 14 (skipping 13)")
            self.elevator.move_to_floor(14)
        elif self.elevator.moving:
            print("Can't move - elevator is already moving!")
        elif self.elevator.doors_open:
            print("Can't move - close the doors first! (Press E)")
        else:
            print(f"Moving up from floor {current} to {current + 1}")
            self.elevator.move_to_floor(current + 1)
            
    def _move_elevator_down(self):
        """Move elevator down one floor."""
        current = self.elevator.current_floor
        if current <= -1:
            print(f"Can't go down - already at basement (Floor {current})")
        elif current == 14:
            # Skip floor 13 (doesn't exist) when going down
            print(f"Moving down from floor {current} to floor 12 (skipping 13)")
            self.elevator.move_to_floor(12)
        elif self.elevator.moving:
            print("Can't move - elevator is already moving!")
        elif self.elevator.doors_open:
            print("Can't move - close the doors first! (Press E)")
        else:
            print(f"Moving down from floor {current} to {current - 1}")
            self.elevator.move_to_floor(current - 1)
            
    def _update_npcs(self, dt):
        """Update all NPCs."""
        for npc in self.npcs[:]:
            npc.update(dt)
            
            # Remove NPCs that have lost patience
            if npc.patience <= 0 and not npc.in_elevator:
                self.npcs.remove(npc)
                # Penalty for making NPCs wait too long
                self.score -= 10
                if npc.npc_type == "good":
                    self.harmony_level = max(0, self.harmony_level - 5)
                elif npc.npc_type == "evil":
                    self.chaos_level = min(100, self.chaos_level + 5)
                    
            # Check for NPC interactions in elevator
            if npc.in_elevator:
                for other_npc in self.elevator.passengers:
                    if other_npc != npc:
                        npc.interact_with(other_npc)
                        
    def _spawn_npcs(self, dt):
        """Spawn new NPCs at random floors."""
        self.spawn_timer -= dt
        
        if self.spawn_timer <= 0:
            self.spawn_timer = self.spawn_interval
            
            # Determine NPC type based on game balance
            npc_type = self._determine_npc_type()
            
            # Choose spawn floor
            spawn_floor = random.choice(list(self.floors.keys()))
            floor = self.floors[spawn_floor]
            
            # Create NPC
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = floor.y - NPC_HEIGHT
            
            if npc_type == "good":
                npc = GoodRobot(x, y)
            elif npc_type == "evil":
                npc = EvilRobot(x, y)
            else:
                npc = NPC(x, y, npc_type)
                
            npc.current_floor = spawn_floor
            self.npcs.append(npc)
            floor.add_waiting_npc(npc)
            
            # Adjust spawn rate based on chaos
            self.spawn_interval = max(1.0, NPC_SPAWN_RATE - (self.chaos_level * 0.02))
            
    def _determine_npc_type(self):
        """Determine what type of NPC to spawn based on game state."""
        # More evil robots spawn as chaos increases
        evil_chance = 0.2 + (self.chaos_level / 200)
        # More good robots spawn to counter evil
        good_chance = 0.2 + (self.chaos_level / 150)
        
        rand = random.random()
        if rand < evil_chance:
            return "evil"
        elif rand < evil_chance + good_chance:
            return "good"
        else:
            return "neutral"
            
    def _update_john(self, dt):
        """Update John the Doorman special character."""
        if self.john_the_doorman is None:
            self.spawn_john_timer -= dt
            if self.spawn_john_timer <= 0:
                # Spawn John at street level
                floor = self.floors[0]
                self.john_the_doorman = NPC(SCREEN_WIDTH // 2, floor.y - NPC_HEIGHT, "neutral")
                self.john_the_doorman.name = "John"
                self.john_the_doorman.color = (50, 50, 150)  # Special blue uniform
                self.john_the_doorman.destination_floor = random.choice([1, 2, 3])
                self.john_the_doorman.patience = 999  # John is very patient
                self.john_the_doorman.current_floor = 0
                self.npcs.append(self.john_the_doorman)
                floor.add_waiting_npc(self.john_the_doorman)
                
                # John's appearance is special
                self.flash_color = BLUE
                self.flash_timer = 0.5
                
    def _update_alan(self, dt):
        """Update Alan the robot mastermind on Floor 4."""
        if self.alan_the_mastermind is None:
            self.spawn_alan_timer -= dt
            if self.spawn_alan_timer <= 0:
                # Spawn Alan at Floor 4 (Robotics Lab)
                if 4 in self.floors:
                    floor = self.floors[4]
                    self.alan_the_mastermind = NPC(SCREEN_WIDTH // 2 - 100, floor.y - NPC_HEIGHT, "good")
                    self.alan_the_mastermind.name = "Alan"
                    self.alan_the_mastermind.color = (0, 200, 255)  # Bright cyan for Alan
                    self.alan_the_mastermind.destination_floor = random.choice([8, 9, 11])  # AI/Biotech floors
                    self.alan_the_mastermind.patience = 999  # Alan is very patient
                    self.alan_the_mastermind.current_floor = 4
                    self.npcs.append(self.alan_the_mastermind)
                    floor.add_waiting_npc(self.alan_the_mastermind)
                    
                    # Alan's appearance is special
                    self.flash_color = CYAN
                    self.flash_timer = 0.5
                    
    def _update_escaped_robots(self, dt):
        """Update bad robots that escape from the basement."""
        # Randomly spawn escaping bad robots from basement
        if random.random() < 0.001:  # Low chance per frame
            # Create a bad robot that's escaping from basement
            if -1 in self.floors:
                floor = self.floors[-1]
                bad_robot = EvilRobot(random.randint(100, SCREEN_WIDTH - 100), floor.y - NPC_HEIGHT)
                bad_robot.name = "Escaped Robot"
                bad_robot.destination_floor = random.choice([0, 1, 2, 3])  # Try to escape to upper floors
                bad_robot.current_floor = -1
                bad_robot.patience = 60  # Very impatient when escaping
                bad_robot.enter_rage_mode()  # Already in rage from fighting
                self.npcs.append(bad_robot)
                floor.add_waiting_npc(bad_robot)
                self.escaped_bad_robots.append(bad_robot)
                
                # Alert effect
                self.screen_shake = 3
                self.chaos_level = min(100, self.chaos_level + 10)
                
    def _handle_elevator_arrivals(self):
        """Handle NPCs entering/exiting elevator when it arrives at floors."""
        if not self.elevator.moving and self.elevator.doors_open:
            current_floor = self.elevator.current_floor
            
            if current_floor in self.floors:
                floor = self.floors[current_floor]
                
                # NPCs exit if this is their destination
                for npc in self.elevator.passengers[:]:
                    if npc.destination_floor == current_floor:
                        npc.exit_elevator(self.elevator)
                        self.npcs.remove(npc)
                        
                        # Score based on delivery
                        self._score_delivery(npc, current_floor)
                        
                # NPCs enter if there's room
                for npc in floor.waiting_npcs[:]:
                    if not self.elevator.is_full():
                        if npc.enter_elevator(self.elevator):
                            floor.remove_waiting_npc(npc)
                            
    def _score_delivery(self, npc, floor_num):
        """Score points for delivering NPCs."""
        base_score = 10
        
        # Bonus for delivering to correct thematic floor
        if npc.npc_type == "good" and floor_num == 4:
            # Good robot delivered to Good Robot Lab
            base_score += 20
            self.harmony_level = min(100, self.harmony_level + 10)
            self.flash_color = CYAN
            self.flash_timer = 0.3
        elif npc.npc_type == "evil" and floor_num == -1:
            # Evil robot delivered to Fight Club
            base_score += 15
            self.chaos_level = min(100, self.chaos_level + 5)
            self.flash_color = RED
            self.flash_timer = 0.3
        elif floor_num == 17:  # Roof rave escape
            # Anyone escaping to the secret roof rave
            base_score += 30
            self.harmony_level = min(100, self.harmony_level + 10)
            self.flash_color = MAGENTA
            self.flash_timer = 0.5
        elif floor_num == 6:  # Arts & Music
            # Bonus for creative floors
            base_score += 15
            self.harmony_level = min(100, self.harmony_level + 3)
            
        # Special bonus for John
        if hasattr(npc, 'name') and npc.name == "John":
            base_score += 50
            self.harmony_level = min(100, self.harmony_level + 20)
            # John will respawn later
            self.spawn_john_timer = random.uniform(10, 20)
            self.john_the_doorman = None
            
        # Special bonus for Alan
        if hasattr(npc, 'name') and npc.name == "Alan":
            base_score += 75
            self.harmony_level = min(100, self.harmony_level + 30)
            # Alan will respawn later
            self.spawn_alan_timer = random.uniform(15, 25)
            self.alan_the_mastermind = None
            
        # Penalty for escaped bad robots reaching upper floors
        if hasattr(npc, 'name') and npc.name == "Escaped Robot":
            if floor_num > 0:
                base_score -= 20  # Penalty for letting them escape
                self.chaos_level = min(100, self.chaos_level + 15)
                self.screen_shake = 5
            
        self.score += base_score
        self.passengers_delivered += 1
        
    def _update_game_balance(self, dt):
        """Update game balance between chaos and harmony."""
        # Natural decay
        self.chaos_level = max(0, self.chaos_level - dt * 0.5)
        self.harmony_level = max(0, self.harmony_level - dt * 0.3)
        
        # Effects of imbalance
        if self.chaos_level > 75:
            # High chaos - more screen shake
            self.screen_shake = min(5, self.screen_shake + dt * 10)
            self.elevator.emergency_mode = True
        else:
            self.elevator.emergency_mode = False
            
        if self.harmony_level > 75:
            # High harmony - bonus spawn rate
            self.spawn_interval = max(0.5, self.spawn_interval - dt * 0.1)
            
    def draw(self, screen):
        """Draw the scene.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Apply screen shake
        shake_offset = [0, 0]
        if self.screen_shake > 0:
            shake_offset[0] = random.randint(-int(self.screen_shake), int(self.screen_shake))
            shake_offset[1] = random.randint(-int(self.screen_shake), int(self.screen_shake))
            
        # Create drawing surface
        draw_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        draw_surface.fill(BLACK)
        
        # Draw background gradient based on game state
        self._draw_background(draw_surface)
        
        # Create a scrollable surface for game objects (extended for 19 floors total)
        game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT * 3))
        game_surface.fill((0, 0, 0, 0))
        
        # Draw elevator shaft (extended for all floors from -1 to 17)
        shaft_rect = pygame.Rect(SHAFT_X, -SCREEN_HEIGHT * 2 + int(self.camera_y), SHAFT_WIDTH, SCREEN_HEIGHT * 3)
        pygame.draw.rect(game_surface, DARK_GRAY, shaft_rect)
        pygame.draw.rect(game_surface, GRAY, shaft_rect, 3)
        
        # Draw floors with camera offset
        for floor_num, floor in self.floors.items():
            # Adjust floor drawing position based on camera
            floor_y = floor.y + int(self.camera_y)
            if -100 < floor_y < SCREEN_HEIGHT + 100:  # Only draw visible floors
                # Create temporary floor rect with camera offset
                temp_floor = Floor(floor_num, floor_y)
                temp_floor.waiting_npcs = floor.waiting_npcs
                temp_floor.ambient_particles = floor.ambient_particles
                temp_floor.glow_intensity = floor.glow_intensity
                temp_floor.light_flicker = floor.light_flicker
                temp_floor.effect_timer = floor.effect_timer
                temp_floor.draw(draw_surface)
            
        # Draw elevator with camera offset
        # Save original position
        original_y = self.elevator.rect.y
        self.elevator.rect.y = int(self.elevator.y + self.camera_y)
        self.elevator.draw(draw_surface)
        self.elevator.rect.y = original_y  # Restore original position
        
        # Draw NPCs with camera offset
        for npc in self.npcs:
            if not npc.in_elevator:
                # Save original position
                original_npc_y = npc.rect.y
                npc.rect.y = int(npc.y + self.camera_y)
                # Only draw if visible
                if -50 < npc.rect.y < SCREEN_HEIGHT + 50:
                    npc.draw(draw_surface)
                npc.rect.y = original_npc_y  # Restore
                
        # Draw UI
        self._draw_ui(draw_surface)
        
        # Apply flash effect
        if self.flash_timer > 0 and self.flash_color:
            flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash_surface.set_alpha(int(100 * self.flash_timer))
            flash_surface.fill(self.flash_color)
            draw_surface.blit(flash_surface, (0, 0))
            
        # Draw tutorial
        if self.show_tutorial:
            self._draw_tutorial(draw_surface)
            
        # Blit to screen with shake
        screen.blit(draw_surface, shake_offset)
        
    def _draw_background(self, screen):
        """Draw dynamic background based on game state."""
        # Create gradient based on chaos/harmony
        for y in range(0, SCREEN_HEIGHT, 10):
            progress = y / SCREEN_HEIGHT
            
            # Base color
            r = int(20 + self.chaos_level * 0.5)
            g = int(20 + self.harmony_level * 0.3)
            b = int(30 + self.harmony_level * 0.5)
            
            # Add gradient
            r = min(255, r + int(progress * 30))
            g = min(255, g + int(progress * 20))
            b = min(255, b + int(progress * 40))
            
            pygame.draw.rect(screen, (r, g, b), (0, y, SCREEN_WIDTH, 10))
            
    def _draw_ui(self, screen):
        """Draw UI elements."""
        font_large = pygame.font.Font(None, 36)
        font_medium = pygame.font.Font(None, 24)
        
        # Score
        score_text = font_large.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (20, 20))
        
        # Passengers delivered
        delivered_text = font_medium.render(f"Delivered: {self.passengers_delivered}", True, YELLOW)
        screen.blit(delivered_text, (20, 60))
        
        # Chaos/Harmony meters
        self._draw_meter(screen, 20, 100, self.chaos_level, "CHAOS", RED)
        self._draw_meter(screen, 20, 140, self.harmony_level, "HARMONY", CYAN)
        
        # Controls hint (Player 1)
        controls_text = font_medium.render("W/S: Move | E: Doors", True, WHITE)
        screen.blit(controls_text, (20, SCREEN_HEIGHT - 40))
        
        # Elevator status
        if self.elevator.doors_open:
            status_text = font_medium.render("Doors OPEN - Press E to close", True, YELLOW)
        elif self.elevator.moving:
            status_text = font_medium.render("Moving...", True, GREEN)
        else:
            status_text = font_medium.render("Ready - Press W/S to move", True, GREEN)
        status_rect = status_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        screen.blit(status_text, status_rect)
        
        # Player 2 controls if applicable
        if self.player_count == 2:
            p2_text = font_medium.render("↑/↓: Move | RShift: Doors", True, YELLOW)
            screen.blit(p2_text, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 40))
            
        # Special character indicator
        if self.john_the_doorman:
            john_text = font_medium.render("John is waiting!", True, BLUE)
            john_rect = john_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
            screen.blit(john_text, john_rect)
            
        # Alan indicator
        if self.alan_the_mastermind:
            alan_text = font_medium.render("Alan needs transport!", True, CYAN)
            alan_rect = alan_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
            screen.blit(alan_text, alan_rect)
            
        # Escaped robot warning
        if self.escaped_bad_robots:
            warning_text = font_medium.render(f"⚠ {len(self.escaped_bad_robots)} ROBOTS ESCAPING! ⚠", True, RED)
            warning_rect = warning_text.get_rect(center=(SCREEN_WIDTH // 2, 110))
            screen.blit(warning_text, warning_rect)
            
    def _draw_meter(self, screen, x, y, value, label, color):
        """Draw a meter bar."""
        font = pygame.font.Font(None, 20)
        
        # Label
        label_text = font.render(label, True, WHITE)
        screen.blit(label_text, (x, y))
        
        # Bar background
        bar_rect = pygame.Rect(x + 80, y, 100, 20)
        pygame.draw.rect(screen, DARK_GRAY, bar_rect)
        
        # Bar fill
        fill_width = int((value / 100) * 100)
        fill_rect = pygame.Rect(x + 80, y, fill_width, 20)
        pygame.draw.rect(screen, color, fill_rect)
        
        # Bar border
        pygame.draw.rect(screen, WHITE, bar_rect, 1)
        
    def _draw_tutorial(self, screen):
        """Draw tutorial hints."""
        if self.tutorial_timer > 0:
            font = pygame.font.Font(None, 24)
            alpha = min(255, int(self.tutorial_timer * 50))
            
            hints = [
                "Operate the elevator between good and evil!",
                "Floor 4: Good Robot Lab - Where love conquers",
                "Basement: Evil Fight Club - Chaos reigns",
                "Deliver NPCs to their destinations for points!"
            ]
            
            y_offset = SCREEN_HEIGHT // 2 - 60
            for hint in hints:
                text = font.render(hint, True, WHITE)
                text.set_alpha(alpha)
                rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                screen.blit(text, rect)
                y_offset += 30
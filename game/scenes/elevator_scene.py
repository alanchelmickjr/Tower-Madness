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
from game.entities.special_npcs import create_special_npc
from game.events.disasters import FloodDisaster
from game.events.hackathon import HackathonEvent
from game.core.ai_sprite_generator import get_sprite_generator

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
        # Position elevator so it sits ON the floor line, not in the middle of the floor
        elevator_y = SCREEN_HEIGHT - 200 - ELEVATOR_HEIGHT + 10  # Align bottom with floor line
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
        self.spawn_timer = 1.0  # Start spawning after 1 second
        self.spawn_interval = NPC_SPAWN_RATE
        self.special_npc_timer = 3.0  # Spawn special NPCs regularly
        self.sprite_generator = get_sprite_generator()
        
        # Game state
        self.score = 0
        self.passengers_delivered = 0
        self.chaos_level = 0  # Increases with evil robot activity
        self.harmony_level = 0  # Increases with good robot activity
        
        # Special characters
        self.special_npcs = {}
        self.spawn_special_timer = 2.0  # Start spawning specials after 2 seconds
        self.escaped_bad_robots = []  # Track bad robots escaping from basement
        
        # Events and disasters
        self.flood_disaster = FloodDisaster()
        self.hackathon_event = HackathonEvent()
        
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
        
        # General timer for animations
        self.timer = 0
        
    def update(self, dt, events):
        """Update the scene.
        
        Args:
            dt: Delta time in seconds
            events: List of pygame events
        """
        # Update timer
        self.timer += dt
        
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
        
        # Spawn special NPCs
        self._spawn_special_npcs(dt)
        
        # Update events
        self.hackathon_event.update(dt, self.elevator, self.npcs, self.floors)
        self.flood_disaster.update(dt, self.elevator, self.npcs)
        
        # Trigger disasters based on chaos level
        if self.chaos_level > 50 and not self.flood_disaster.active:
            if random.random() < 0.001 * (self.chaos_level / 100):
                self.flood_disaster.trigger_flood()
        
        # Hackathon causes Floor 2 jamming
        if self.hackathon_event.check_elevator_at_floor_2(self.elevator):
            # Spawn extra NPCs going to street level
            if random.random() < 0.3:
                self._spawn_hackathon_jammer()
        
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
        elif current == 0:
            # Skip floor 1 (doesn't exist) - go from 0 to 2
            print(f"Moving up from floor {current} to floor 2 (skipping 1)")
            self.elevator.move_to_floor(2)
        elif current == 12:
            # Skip floor 13 (doesn't exist)
            print(f"Moving up from floor {current} to floor 14 (skipping 13)")
            self.elevator.move_to_floor(14)
        elif self.elevator.moving:
            print("Can't move - elevator is already moving!")
        elif self.elevator.doors_open:
            print("Can't move - close the doors first! (Press E)")
        else:
            # Check if next floor exists
            next_floor = current + 1
            if next_floor not in FLOORS:
                print(f"ERROR: Floor {next_floor} doesn't exist!")
            else:
                print(f"Moving up from floor {current} to {next_floor}")
                self.elevator.move_to_floor(next_floor)
            
    def _move_elevator_down(self):
        """Move elevator down one floor."""
        current = self.elevator.current_floor
        if current <= -1:
            print(f"Can't go down - already at basement (Floor {current})")
        elif current == 2:
            # Skip floor 1 (doesn't exist) when going down - go from 2 to 0
            print(f"Moving down from floor {current} to floor 0 (skipping 1)")
            self.elevator.move_to_floor(0)
        elif current == 14:
            # Skip floor 13 (doesn't exist) when going down
            print(f"Moving down from floor {current} to floor 12 (skipping 13)")
            self.elevator.move_to_floor(12)
        elif self.elevator.moving:
            print("Can't move - elevator is already moving!")
        elif self.elevator.doors_open:
            print("Can't move - close the doors first! (Press E)")
        else:
            # Check if previous floor exists
            prev_floor = current - 1
            if prev_floor not in FLOORS:
                print(f"ERROR: Floor {prev_floor} doesn't exist!")
            else:
                print(f"Moving down from floor {current} to {prev_floor}")
                self.elevator.move_to_floor(prev_floor)
            
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
            # Increase spawn rate with chaos
            self.spawn_timer = max(0.5, self.spawn_interval - (self.chaos_level * 0.01))
            
            # Spawn multiple NPCs when chaos is high
            spawn_count = 1
            if self.chaos_level > 30:
                spawn_count = 2
            if self.chaos_level > 60:
                spawn_count = 3
            
            for _ in range(spawn_count):
                # Determine NPC type based on game balance
                npc_type = self._determine_npc_type()
                
                # Choose spawn floor (avoid floor 1 since it doesn't exist)
                available_floors = [f for f in self.floors.keys() if f != 1]
                spawn_floor = random.choice(available_floors)
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
                # Avoid floor 1 as destination
                possible_destinations = [f for f in self.floors.keys() if f != 1 and f != spawn_floor]
                npc.destination_floor = random.choice(possible_destinations)
                
                self.npcs.append(npc)
                floor.add_waiting_npc(npc)
            
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
            
    def _spawn_special_npcs(self, dt):
        """Spawn special named NPCs on their floors."""
        self.special_npc_timer -= dt
        
        if self.special_npc_timer <= 0:
            self.special_npc_timer = random.uniform(5, 15)  # Random interval
            
            # List of special NPCs and their floors
            special_spawns = [
                (0, "John"),  # Street level
                (2, "Xeno"),  # Event space
                (3, "Vitalia"),  # Private offices
                (4, random.choice(["Vitaly", "Xenia", "Alan"])),  # Robotics
                (6, "Scott"),  # Arts & Music
                (7, random.choice(["Tony", "Cindy"])),  # Maker Space
                (8, "Morgan"),  # Biotech
                (9, "Devinder"),  # AI
                (10, "China"),  # Accelerator
                (11, "Laurence"),  # Health
                (16, "Xeno"),  # d/acc Lounge
            ]
            
            # Pick a random special to spawn
            floor_num, npc_name = random.choice(special_spawns)
            
            # Don't spawn if already exists
            if npc_name not in self.special_npcs or self.special_npcs[npc_name] not in self.npcs:
                if floor_num in self.floors:
                    floor = self.floors[floor_num]
                    x = random.randint(100, SCREEN_WIDTH - 100)
                    y = floor.y - NPC_HEIGHT
                    
                    special_npc = create_special_npc(floor_num, x, y)
                    if special_npc:
                        # Set proper destination (avoid floor 1)
                        possible_destinations = [f for f in self.floors.keys() if f != 1 and f != floor_num]
                        special_npc.destination_floor = random.choice(possible_destinations)
                        
                        self.npcs.append(special_npc)
                        floor.add_waiting_npc(special_npc)
                        self.special_npcs[npc_name] = special_npc
                        
                        # Special effect
                        self.flash_color = special_npc.special_color if hasattr(special_npc, 'special_color') else WHITE
                        self.flash_timer = 0.3
                        
        # Spawn Headphone James during disasters
        if (self.flood_disaster.active or self.chaos_level > 80) and "HeadphoneJames" not in self.special_npcs:
            if random.random() < 0.01:  # Chance to appear
                floor_num = random.choice(list(self.floors.keys()))
                floor = self.floors[floor_num]
                x = SCREEN_WIDTH // 2
                y = floor.y - NPC_HEIGHT
                
                # Create Headphone James to save the day
                james = create_special_npc(floor_num, x, y)
                if james:
                    james.name = "HeadphoneJames"
                    james.patience = 999
                    self.npcs.append(james)
                    floor.add_waiting_npc(james)
                    self.special_npcs["HeadphoneJames"] = james
                    
                    # Epic entrance
                    self.flash_color = MAGENTA
                    self.flash_timer = 1.0
                    self.screen_shake = 10
                    
    def _spawn_hackathon_jammer(self):
        """Spawn NPCs at Floor 2 going to street level during hackathon."""
        if 2 in self.floors and 0 in self.floors:
            floor = self.floors[2]
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = floor.y - NPC_HEIGHT
            
            jammer = NPC(x, y, "neutral")
            jammer.name = f"Hacker{random.randint(100, 999)}"
            jammer.current_floor = 2
            jammer.destination_floor = 0  # Going to street level
            jammer.patience = 20  # Impatient
            jammer.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            
            self.npcs.append(jammer)
            floor.add_waiting_npc(jammer)
            
            # Increase chaos
            self.chaos_level = min(100, self.chaos_level + 2)
                
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
            
        # Draw disaster effects
        self.flood_disaster.draw(draw_surface, int(self.camera_y))
        self.hackathon_event.draw(draw_surface)
        
        # Blit to screen with shake (including disaster shake)
        disaster_shake = self.flood_disaster.get_shake_offset()
        total_shake = (shake_offset[0] + disaster_shake[0], shake_offset[1] + disaster_shake[1])
        screen.blit(draw_surface, total_shake)
        
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
        font_small = pygame.font.Font(None, 20)
        
        # Draw main goal panel at top
        goal_bg = pygame.Rect(10, 10, 350, 180)
        pygame.draw.rect(screen, (0, 0, 0, 200), goal_bg)
        pygame.draw.rect(screen, CYAN, goal_bg, 3)
        
        # Title
        title_text = font_large.render("🏢 ELEVATOR OPERATOR 🏢", True, YELLOW)
        screen.blit(title_text, (20, 20))
        
        # Score with emphasis
        score_text = font_large.render(f"SCORE: {self.score}", True, WHITE)
        screen.blit(score_text, (20, 55))
        
        # Passengers delivered with goal
        goal_text = "Goal: Deliver 20 passengers!"
        if self.passengers_delivered >= 20:
            goal_text = "🎉 GOAL REACHED! Keep going! 🎉"
            delivered_color = GREEN
        elif self.passengers_delivered >= 15:
            delivered_color = YELLOW
        else:
            delivered_color = WHITE
            
        delivered_text = font_medium.render(f"Delivered: {self.passengers_delivered}/20", True, delivered_color)
        screen.blit(delivered_text, (20, 90))
        
        goal_surface = font_small.render(goal_text, True, delivered_color)
        screen.blit(goal_surface, (20, 115))
        
        # Chaos/Harmony meters with explanations
        self._draw_meter(screen, 20, 140, self.chaos_level, "CHAOS", RED)
        chaos_hint = font_small.render("(Too high = disasters!)", True, GRAY)
        screen.blit(chaos_hint, (200, 142))
        
        self._draw_meter(screen, 20, 165, self.harmony_level, "HARMONY", CYAN)
        harmony_hint = font_small.render("(Keep this high!)", True, GRAY)
        screen.blit(harmony_hint, (200, 167))
        
        # Draw controls panel at bottom with better visibility
        controls_bg = pygame.Rect(10, SCREEN_HEIGHT - 120, SCREEN_WIDTH - 20, 110)
        pygame.draw.rect(screen, (0, 0, 0, 200), controls_bg)
        pygame.draw.rect(screen, GREEN, controls_bg, 2)
        
        # Controls title
        controls_title = font_medium.render("🎮 CONTROLS 🎮", True, YELLOW)
        controls_rect = controls_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 105))
        screen.blit(controls_title, controls_rect)
        
        # Control instructions
        control_lines = [
            "W/↑: Go UP one floor | S/↓: Go DOWN one floor",
            "E/SPACE: Open/Close Doors (must be stopped!)",
            "Pick up waiting NPCs → Deliver to their floor → Score points!"
        ]
        
        y_offset = SCREEN_HEIGHT - 75
        for line in control_lines:
            text = font_small.render(line, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 22
        
        # Elevator status with big visibility
        status_bg = pygame.Rect(SCREEN_WIDTH - 250, 20, 230, 60)
        pygame.draw.rect(screen, BLACK, status_bg)
        
        if self.elevator.doors_open:
            status_text = "🚪 DOORS OPEN"
            status_color = YELLOW
            pygame.draw.rect(screen, YELLOW, status_bg, 3)
        elif self.elevator.moving:
            status_text = "⬆️ MOVING..."
            status_color = GREEN
            pygame.draw.rect(screen, GREEN, status_bg, 3)
        else:
            status_text = "✅ READY"
            status_color = CYAN
            pygame.draw.rect(screen, CYAN, status_bg, 3)
            
        status_surface = font_medium.render(status_text, True, status_color)
        status_rect = status_surface.get_rect(center=(status_bg.centerx, status_bg.centery))
        screen.blit(status_surface, status_rect)
        
        # Player 2 controls if applicable
        if self.player_count == 2:
            p2_text = font_medium.render("↑/↓: Move | RShift: Doors", True, YELLOW)
            screen.blit(p2_text, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 40))
            
        # Special character indicators with better visibility
        special_count = len([npc for npc in self.special_npcs.values() if npc in self.npcs])
        if special_count > 0:
            special_bg = pygame.Rect(SCREEN_WIDTH // 2 - 150, 200, 300, 30)
            pygame.draw.rect(screen, BLACK, special_bg)
            pygame.draw.rect(screen, GOLD, special_bg, 2)
            
            special_text = font_medium.render(f"🌟 {special_count} VIP NPCs waiting! 🌟", True, GOLD)
            special_rect = special_text.get_rect(center=(SCREEN_WIDTH // 2, 215))
            screen.blit(special_text, special_rect)
        
        # NPCs waiting on each floor indicator
        waiting_by_floor = {}
        for npc in self.npcs:
            if not npc.in_elevator and npc.current_floor in self.floors:
                if npc.current_floor not in waiting_by_floor:
                    waiting_by_floor[npc.current_floor] = 0
                waiting_by_floor[npc.current_floor] += 1
        
        if waiting_by_floor:
            # Draw waiting passengers panel
            waiting_bg = pygame.Rect(SCREEN_WIDTH - 180, 100, 170, 20 + len(waiting_by_floor) * 20)
            pygame.draw.rect(screen, (0, 0, 0, 200), waiting_bg)
            pygame.draw.rect(screen, ORANGE, waiting_bg, 2)
            
            waiting_title = font_small.render("WAITING PASSENGERS:", True, ORANGE)
            screen.blit(waiting_title, (SCREEN_WIDTH - 175, 105))
            
            y_pos = 125
            for floor, count in sorted(waiting_by_floor.items()):
                floor_name = f"Floor {floor}"
                if floor == -1:
                    floor_name = "Basement"
                elif floor == 0:
                    floor_name = "Street"
                elif floor == 17:
                    floor_name = "Roof"
                    
                waiting_text = font_small.render(f"{floor_name}: {count}", True, WHITE)
                screen.blit(waiting_text, (SCREEN_WIDTH - 170, y_pos))
                y_pos += 18
            
        # Hackathon indicator with timer
        if self.hackathon_event.active:
            hack_bg = pygame.Rect(SCREEN_WIDTH // 2 - 180, 240, 360, 35)
            pygame.draw.rect(screen, BLACK, hack_bg)
            pygame.draw.rect(screen, ORANGE if int(self.timer * 4) % 2 == 0 else YELLOW, hack_bg, 3)
            
            time_left = max(0, self.hackathon_event.duration - self.hackathon_event.timer)
            hack_text = font_medium.render(f"💻 HACKATHON FLOOR 2! Time: {time_left:.0f}s 💻", True,
                                         YELLOW if int(self.timer * 4) % 2 == 0 else ORANGE)
            hack_rect = hack_text.get_rect(center=(SCREEN_WIDTH // 2, 257))
            screen.blit(hack_text, hack_rect)
            
        # Flood warning with urgency
        if self.flood_disaster.active:
            flood_bg = pygame.Rect(SCREEN_WIDTH // 2 - 180, 280, 360, 35)
            pygame.draw.rect(screen, BLACK, flood_bg)
            pygame.draw.rect(screen, BLUE if int(self.timer * 4) % 2 == 0 else CYAN, flood_bg, 3)
            
            flood_text = font_medium.render("🌊 FLOOD! GET EVERYONE UP! 🌊", True,
                                          CYAN if int(self.timer * 4) % 2 == 0 else BLUE)
            flood_rect = flood_text.get_rect(center=(SCREEN_WIDTH // 2, 297))
            screen.blit(flood_text, flood_rect)
            
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
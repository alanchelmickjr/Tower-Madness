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
from game.events.disasters import FloodDisaster, PowerOutage
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
        
        # Tower Funds Life System
        self.tower_funds = 10000
        self.max_tower_funds = 10000
        self.funds_drain_rate = 0.0108
        self.low_funds_threshold = 3000
        
        # Elevator Operator Stress System
        self.operator_stress = 0
        self.max_operator_stress = 100
        self.stress_threshold_warning = 70
        self.stress_threshold_quit = 100
        
        # 5-Minute Game Timer
        self.game_time_limit = 300.0  # 5 minutes in seconds
        self.time_remaining = self.game_time_limit
        self.delivery_goal = 15  # Reduced from 20 for 5-min sessions
        
        # Special characters
        self.special_npcs = {}
        self.spawn_special_timer = 2.0  # Start spawning specials after 2 seconds
        self.escaped_bad_robots = []  # Track bad robots escaping from basement
        
        # Events and disasters
        self.flood_disaster = FloodDisaster()
        self.hackathon_event = HackathonEvent()
        self.power_outage = PowerOutage()
        
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
        
        # Debug disaster buttons (for demo/testing)
        self.debug_mode = True  # Enable for demos
        self.flood_button = pygame.Rect(SCREEN_WIDTH - 220, 15, 90, 30)
        self.hackathon_button = pygame.Rect(SCREEN_WIDTH - 120, 15, 90, 30)
        self.power_outage_button = pygame.Rect(SCREEN_WIDTH - 320, 15, 90, 30)
        
    def update(self, dt, events):
        """Update the scene.
        
        Args:
            dt: Delta time in seconds
            events: List of pygame events
        """
        # Update timer
        self.timer += dt
        
        # Countdown game timer
        self.time_remaining -= dt
        if self.time_remaining <= 0:
            self.time_remaining = 0
            # Time's up - check if goal reached
            from game.core.constants import STATE_GAME_OVER
            return STATE_GAME_OVER
        
        # Check for funds depletion game over
        if self._update_tower_funds(dt):
            from game.core.constants import STATE_GAME_OVER
            return STATE_GAME_OVER
        
        # Check operator stress
        if self.operator_stress >= self.stress_threshold_quit:
            from game.core.constants import STATE_GAME_OVER
            return STATE_GAME_OVER
        
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
        hackathon_was_active = self.hackathon_event.active
        self.hackathon_event.update(dt, self.elevator, self.npcs, self.floors)
        
        # Reset chaos when hackathon ends
        if hackathon_was_active and not self.hackathon_event.active:
            self.chaos_level = max(0, self.chaos_level - 50)
        
        self.flood_disaster.update(dt, self.elevator, self.npcs)
        self.power_outage.update(dt)
        
        # Trigger disasters based on chaos level (balanced frequency)
        if self.chaos_level > 50 and not self.flood_disaster.active:
            if random.random() < 0.001 * (self.chaos_level / 100):  # Slowed down 2x
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
                elif event.key == PLAYER1_CONTROLS["open_doors"] or event.key == PLAYER1_CONTROLS["action"]:
                    print(f"Toggling doors. Current state: {self.elevator.doors_open}")
                    self.elevator.toggle_doors()
                    
                # Player 2 controls (if 2-player mode)
                if self.player_count == 2:
                    if event.key == PLAYER2_CONTROLS["up"]:
                        self._move_elevator_up()
                    elif event.key == PLAYER2_CONTROLS["down"]:
                        self._move_elevator_down()
                    elif event.key == PLAYER2_CONTROLS["open_doors"] or event.key == PLAYER2_CONTROLS["action"]:
                        self.elevator.toggle_doors()
                        
            # Mouse clicks for debug buttons
            elif event.type == pygame.MOUSEBUTTONDOWN and self.debug_mode:
                mouse_pos = event.pos
                if self.flood_button.collidepoint(mouse_pos):
                    if not self.flood_disaster.active:
                        self.flood_disaster.trigger_flood()
                        print("🌊 FLOOD triggered via debug button!")
                elif self.hackathon_button.collidepoint(mouse_pos):
                    if not self.hackathon_event.active:
                        self.hackathon_event.trigger()
                        print("💻 HACKATHON triggered via debug button!")
                elif self.power_outage_button.collidepoint(mouse_pos):
                    if not self.power_outage.active:
                        self.power_outage.trigger()
                        print("⚡ POWER OUTAGE triggered via debug button!")
                        
    def _move_elevator_up(self):
        """Move elevator up one floor."""
        # Check if power outage has disabled elevator
        if self.power_outage.elevator_disabled:
            print("⚡ Elevator disabled during power outage!")
            return
            
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
        # Check if power outage has disabled elevator
        if self.power_outage.elevator_disabled:
            print("⚡ Elevator disabled during power outage!")
            return
            
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
                # Check before removing to avoid ValueError
                if npc in self.npcs:
                    self.npcs.remove(npc)
                # Penalty for making NPCs wait too long
                self.score -= 10
                self.tower_funds -= 15  # NPC leaves, cancels membership (original penalty)
                self.operator_stress += 0.5  # Much slower stress buildup
                
                # Warning message when funds drop below threshold
                if self.tower_funds <= self.low_funds_threshold and self.tower_funds > 0:
                    print(f"⚠️ LOW FUNDS WARNING! Tower funds: ${int(self.tower_funds)}")
                
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
                (3, "Sophia"),  # Private offices
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
                        # Only remove if still in list (avoid ValueError)
                        if npc in self.npcs:
                            self.npcs.remove(npc)
                        
                        # Score based on delivery
                        self._score_delivery(npc, current_floor)
                        
                # NPCs enter if there's room
                for npc in floor.waiting_npcs[:]:
                    if not self.elevator.is_full():
                        if npc.enter_elevator(self.elevator):
                            floor.remove_waiting_npc(npc)
                            
                            # Special: Xeno resolves all disasters when picked up!
                            if hasattr(npc, 'name') and npc.name == "Xeno":
                                self._xeno_resolves_all()
                            
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
        
        self.tower_funds = min(self.tower_funds + 50, self.max_tower_funds)  # Restore funds
        
    def _xeno_resolves_all(self):
        """Xeno's special power - resolves all disasters and removes bad robots."""
        print("🌟 XENO PICKED UP! Resolving all disasters! 🌟")
        
        # End flood disaster
        if self.flood_disaster.active:
            self.flood_disaster.active = False
            self.flood_disaster.water_level = 0
            self.flood_disaster.timer = 0
            print("Flood resolved by Xeno's presence!")
            
        # End hackathon event
        if self.hackathon_event.active:
            self.hackathon_event.active = False
            self.hackathon_event.timer = 0
            print("Hackathon peacefully concluded by Xeno!")
            
        # Remove all evil/bad robots
        for npc in self.npcs[:]:
            if npc.npc_type == "evil" or (hasattr(npc, 'name') and "Escaped" in npc.name):
                # Remove from floors first
                if npc.current_floor in self.floors:
                    floor = self.floors[npc.current_floor]
                    if npc in floor.waiting_npcs:
                        floor.remove_waiting_npc(npc)
                # Remove from elevator if present
                if npc in self.elevator.passengers:
                    self.elevator.passengers.remove(npc)
                # Remove from NPCs list (check first to avoid ValueError)
                if npc in self.npcs:
                    self.npcs.remove(npc)
                    
        # Clear escaped bad robots list
        self.escaped_bad_robots.clear()
        
        # Reset chaos level
        self.chaos_level = 0
        
        # Boost harmony
        self.harmony_level = min(100, self.harmony_level + 50)
        
        # Visual celebration
        self.flash_color = GOLD
        self.flash_timer = 1.0
        self.screen_shake = 5
        
        # Bonus score
        self.score += 100
        print("Xeno brings peace! +100 bonus points!")
        
    def _update_game_balance(self, dt):
        """Update game balance between chaos and harmony."""
        # Natural decay
        self.chaos_level = max(0, self.chaos_level - dt * 0.5)
        self.harmony_level = max(0, self.harmony_level - dt * 0.3)
        
        # Effects of imbalance
        if self.chaos_level > 75:
            # High chaos - periodic screen shake instead of continuous
            # Only add shake occasionally to not disrupt gameplay
            if random.random() < 0.01:  # Small chance each frame
                self.screen_shake = min(3, self.screen_shake + 2)  # Smaller shake
            self.elevator.emergency_mode = True
        else:
            self.elevator.emergency_mode = False
            
        if self.harmony_level > 75:
            # High harmony - bonus spawn rate
            self.spawn_interval = max(0.5, self.spawn_interval - dt * 0.1)
        
        # Operator stress naturally decreases quickly
        self.operator_stress = max(0, self.operator_stress - 5.0 * dt)
    
    def _update_tower_funds(self, dt):
        """Update tower funds - drains over time, game over if depleted"""
        drain = self.funds_drain_rate * dt
        
        # Disasters drain funds much faster
        if self.flood_disaster.active:
            drain *= 20  # 20x faster drain during flood
        if self.hackathon_event.active:
            drain *= 10  # 10x faster drain during hackathon
        if self.power_outage.active:
            drain *= 15  # 15x faster drain during power outage
            
        self.tower_funds -= drain
        
        if self.tower_funds <= 0:
            self.tower_funds = 0
            return True  # Trigger game over
        
        return False
            
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
        
        # Draw elevator panel
        self._draw_elevator_panel(draw_surface)
        
        # Apply flash effect (border only to avoid covering UI)
        if self.flash_timer > 0 and self.flash_color:
            border_width = int(20 * self.flash_timer)
            pygame.draw.rect(draw_surface, self.flash_color, (0, 0, SCREEN_WIDTH, border_width))  # Top
            pygame.draw.rect(draw_surface, self.flash_color, (0, SCREEN_HEIGHT - border_width, SCREEN_WIDTH, border_width))  # Bottom
            pygame.draw.rect(draw_surface, self.flash_color, (0, 0, border_width, SCREEN_HEIGHT))  # Left
            pygame.draw.rect(draw_surface, self.flash_color, (SCREEN_WIDTH - border_width, 0, border_width, SCREEN_HEIGHT))  # Right
            
        # Draw tutorial
        if self.show_tutorial:
            self._draw_tutorial(draw_surface)
            
        # Draw disaster effects
        self.flood_disaster.draw(draw_surface, int(self.camera_y))
        self.hackathon_event.draw(draw_surface)
        self.power_outage.draw(draw_surface)
        
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
        """Draw UI elements in retro arcade dashboard style."""
        font_large = pygame.font.Font(None, 36)
        font_medium = pygame.font.Font(None, 24)
        font_small = pygame.font.Font(None, 20)
        font_tiny = pygame.font.Font(None, 16)
        
        # ═══════════════════════════════════════════════════════════
        # TOP: Game Timer - prominent center
        # ═══════════════════════════════════════════════════════════
        minutes = int(self.time_remaining // 60)
        seconds = int(self.time_remaining % 60)
        timer_text = f"{minutes}:{seconds:02d}"

        if self.time_remaining > 180:
            timer_color = GREEN
        elif self.time_remaining > 60:
            timer_color = YELLOW
        else:
            timer_color = RED

        timer_font = pygame.font.Font(None, 48)
        timer_surface = timer_font.render(timer_text, True, timer_color)
        timer_rect = timer_surface.get_rect(center=(SCREEN_WIDTH // 2, 30))

        bg_rect = timer_rect.inflate(20, 10)
        pygame.draw.rect(screen, BLACK, bg_rect)
        pygame.draw.rect(screen, timer_color, bg_rect, 3)
        screen.blit(timer_surface, timer_rect)
        
        # ═══════════════════════════════════════════════════════════
        # LEFT PANEL: Score & Mission Status
        # ═══════════════════════════════════════════════════════════
        left_panel = pygame.Rect(10, 70, 240, 180)
        pygame.draw.rect(screen, (10, 10, 20, 220), left_panel)
        pygame.draw.rect(screen, CYAN, left_panel, 2)
        
        # Score
        score_text = font_large.render(f"SCORE: {self.score}", True, YELLOW)
        screen.blit(score_text, (20, 80))
        
        # Delivered progress
        if self.passengers_delivered >= self.delivery_goal:
            delivered_color = GREEN
        elif self.passengers_delivered >= (self.delivery_goal - 3):
            delivered_color = YELLOW
        else:
            delivered_color = WHITE
            
        delivered_text = font_medium.render(f"DELIVERED: {self.passengers_delivered}/{self.delivery_goal}", True, delivered_color)
        screen.blit(delivered_text, (20, 120))
        
        # Mission goal
        if self.passengers_delivered >= self.delivery_goal:
            goal_text = "✓ GOAL COMPLETE!"
            goal_color = GREEN
        else:
            goal_text = "Deliver 15 in 5 min"
            goal_color = WHITE
        goal_surface = font_small.render(goal_text, True, goal_color)
        screen.blit(goal_surface, (20, 150))
        
        # Funds meter in left panel
        funds_label = font_small.render("TOWER FUNDS", True, CYAN)
        screen.blit(funds_label, (20, 180))
        
        funds_pct = self.tower_funds / self.max_tower_funds
        funds_width = int(200 * funds_pct)
        
        if self.tower_funds > 10000:
            funds_color = GREEN
        elif self.tower_funds > self.low_funds_threshold:
            funds_color = YELLOW
        else:
            funds_color = RED
        
        pygame.draw.rect(screen, (30, 30, 30), (20, 200, 200, 20))
        pygame.draw.rect(screen, funds_color, (20, 200, funds_width, 20))
        pygame.draw.rect(screen, WHITE, (20, 200, 200, 20), 2)
        
        funds_value = font_small.render(f"${int(self.tower_funds)}", True, WHITE)
        screen.blit(funds_value, (20, 225))
        
        # Operator Stress
        if self.operator_stress > self.stress_threshold_warning:
            stress_text = font_small.render("⚠️ OPERATOR STRESS HIGH!", True, (255, 100, 100))
            screen.blit(stress_text, (20, 230))
        
        # ═══════════════════════════════════════════════════════════
        # RIGHT PANEL: Status & Meters
        # ═══════════════════════════════════════════════════════════
        right_panel = pygame.Rect(SCREEN_WIDTH - 250, 70, 240, 180)
        pygame.draw.rect(screen, (10, 10, 20, 220), right_panel)
        pygame.draw.rect(screen, ORANGE, right_panel, 2)
        
        # Elevator status
        if self.elevator.doors_open:
            status_text = "🚪 DOORS OPEN"
            status_color = YELLOW
        elif self.elevator.moving:
            status_text = "⬆️ MOVING"
            status_color = GREEN
        else:
            status_text = "✓ READY"
            status_color = CYAN
            
        status_surface = font_medium.render(status_text, True, status_color)
        screen.blit(status_surface, (SCREEN_WIDTH - 240, 80))
        
        # Chaos meter
        self._draw_compact_meter(screen, SCREEN_WIDTH - 240, 120, self.chaos_level, "CHAOS", RED)
        
        # Harmony meter
        self._draw_compact_meter(screen, SCREEN_WIDTH - 240, 160, self.harmony_level, "HARMONY", CYAN)
        
        # Passenger count
        pass_count = len(self.elevator.passengers)
        pass_color = RED if pass_count >= 6 else YELLOW if pass_count >= 4 else WHITE
        pass_text = font_small.render(f"IN ELEVATOR: {pass_count}/6", True, pass_color)
        screen.blit(pass_text, (SCREEN_WIDTH - 240, 200))
        
        # ═══════════════════════════════════════════════════════════
        # BOTTOM: Controls Panel
        # ═══════════════════════════════════════════════════════════
        controls_bg = pygame.Rect(10, SCREEN_HEIGHT - 40, SCREEN_WIDTH - 20, 35)
        pygame.draw.rect(screen, (10, 10, 20, 220), controls_bg)
        pygame.draw.rect(screen, GREEN, controls_bg, 2)
        
        controls_title = font_tiny.render("🎮 CONTROLS", True, YELLOW)
        screen.blit(controls_title, (20, SCREEN_HEIGHT - 38))
        
        control_lines = [
            "W/↑: UP | S/↓: DOWN | E/SPACE: Doors | Pick up NPCs → Deliver → Score!",
        ]
        
        y_offset = SCREEN_HEIGHT - 22
        for line in control_lines:
            text = font_small.render(line, True, WHITE)
            screen.blit(text, (20, y_offset))
            y_offset += 20
        
        # ═══════════════════════════════════════════════════════════
        # TOP ALERT BANNERS - Compact and consolidated
        # ═══════════════════════════════════════════════════════════
        alert_y = 70  # Start position for alerts
        alert_height = 30
        alert_font = pygame.font.Font(None, 24)  # Compact font size
        
        # Collect all active alerts
        alerts = []
        
        # VIP indicator
        special_count = len([npc for npc in self.special_npcs.values() if npc in self.npcs])
        if special_count > 0:
            alerts.append((f"⭐ {special_count} VIP waiting!", GOLD))
        
        # Hackathon indicator
        if self.hackathon_event.active:
            time_left = max(0, self.hackathon_event.duration - self.hackathon_event.timer)
            alerts.append((f"💻 HACKATHON F2! {time_left:.0f}s", ORANGE))
        
        # Flood warning
        if self.flood_disaster.active:
            alerts.append(("🌊 FLOOD! GET EVERYONE UP!", CYAN))
        
        # Draw all alerts in a single compact banner
        for alert_text, alert_color in alerts:
            alert_bg = pygame.Rect(SCREEN_WIDTH // 2 - 180, alert_y, 360, alert_height)
            pygame.draw.rect(screen, BLACK, alert_bg)
            pygame.draw.rect(screen, alert_color, alert_bg, 2)
            alert_surface = alert_font.render(alert_text, True, alert_color)
            alert_rect = alert_surface.get_rect(center=(SCREEN_WIDTH // 2, alert_y + 15))
            screen.blit(alert_surface, alert_rect)
            alert_y += alert_height + 5  # Stack alerts with small gap
        
        # Draw debug disaster trigger buttons (for demo/testing)
        if self.debug_mode:
            font_small = pygame.font.Font(None, 18)
            
            # Flood button
            flood_color = RED if self.flood_disaster.active else (100, 150, 200)
            pygame.draw.rect(screen, BLACK, self.flood_button)
            pygame.draw.rect(screen, flood_color, self.flood_button, 2)
            flood_text = font_small.render("🌊 FLOOD", True, flood_color)
            flood_rect = flood_text.get_rect(center=self.flood_button.center)
            screen.blit(flood_text, flood_rect)
            
            # Hackathon button
            hack_color = ORANGE if self.hackathon_event.active else (200, 150, 100)
            pygame.draw.rect(screen, BLACK, self.hackathon_button)
            pygame.draw.rect(screen, hack_color, self.hackathon_button, 2)
            hack_text = font_small.render("💻 HACK", True, hack_color)
            hack_rect = hack_text.get_rect(center=self.hackathon_button.center)
            screen.blit(hack_text, hack_rect)
            
            # Power Outage button
            outage_color = YELLOW if self.power_outage.active else (150, 150, 100)
            pygame.draw.rect(screen, BLACK, self.power_outage_button)
            pygame.draw.rect(screen, outage_color, self.power_outage_button, 2)
            outage_text = font_small.render("⚡ POWER", True, outage_color)
            outage_rect = outage_text.get_rect(center=self.power_outage_button.center)
            screen.blit(outage_text, outage_rect)
            
            # Debug label removed - buttons now at top near timer
            
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
    
    def _draw_compact_meter(self, screen, x, y, value, label, color):
        """Draw a compact meter bar for dashboard."""
        font = pygame.font.Font(None, 18)
        
        # Label
        label_text = font.render(label, True, WHITE)
        screen.blit(label_text, (x, y))
        
        # Bar
        bar_width = 140
        bar_height = 16
        bar_rect = pygame.Rect(x + 80, y, bar_width, bar_height)
        pygame.draw.rect(screen, (30, 30, 30), bar_rect)
        
        # Fill
        fill_width = int((value / 100) * bar_width)
        fill_rect = pygame.Rect(x + 80, y, fill_width, bar_height)
        pygame.draw.rect(screen, color, fill_rect)
        
        # Border
        pygame.draw.rect(screen, WHITE, bar_rect, 2)
        
        # Value text
        value_text = font.render(f"{int(value)}", True, WHITE)
        screen.blit(value_text, (x + 225, y))
    
    def _draw_elevator_panel(self, screen):
        """Draw elevator button panel showing floors with waiting passengers"""
        panel_x = SCREEN_WIDTH - 140
        panel_y = 270
        panel_width = 125
        button_height = 25
        
        # Panel background
        pygame.draw.rect(screen, (30, 30, 30), (panel_x, panel_y, panel_width, 500))
        pygame.draw.rect(screen, CYAN, (panel_x, panel_y, panel_width, 500), 2)
        
        # Title (smaller, stacked)
        title_font = pygame.font.Font(None, 18)
        title1 = title_font.render("ELEVATOR", True, CYAN)
        title2 = title_font.render("PANEL", True, CYAN)
        screen.blit(title1, (panel_x + 30, panel_y + 8))
        screen.blit(title2, (panel_x + 35, panel_y + 22))
        
        # Draw buttons for each floor
        y_offset = panel_y + 42
        small_font = pygame.font.Font(None, 20)
        
        for floor_num in sorted(self.floors.keys(), reverse=True):
            if floor_num in [1, 13]:  # Skip non-existent floors
                continue
                
            floor = self.floors[floor_num]
            waiting_count = len(floor.waiting_npcs)
            
            # Button background - highlight if current floor
            button_color = (100, 100, 150) if floor_num == self.elevator.current_floor else (50, 50, 50)
            pygame.draw.rect(screen, button_color, (panel_x + 10, y_offset, panel_width - 20, button_height - 2))
            pygame.draw.rect(screen, WHITE, (panel_x + 10, y_offset, panel_width - 20, button_height - 2), 1)
            
            # Floor label
            floor_name = floor.get_short_name()  # Use floor name if available
            label = small_font.render(floor_name, True, WHITE)
            screen.blit(label, (panel_x + 15, y_offset + 5))
            
            # Waiting indicator - orange dots for waiting passengers
            if waiting_count > 0:
                dots = "●" * min(waiting_count, 3)
                if waiting_count > 3:
                    dots = "●●●+"
                dot_text = small_font.render(dots, True, (255, 165, 0))
                screen.blit(dot_text, (panel_x + panel_width - 50, y_offset + 5))
            
            y_offset += button_height
        
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

"""
Elevator entity for Tower Madness / Elevator Operator
The player-controlled elevator caught between good and evil
"""

import pygame
import random
from game.core.constants import *
from game.core.sound_manager import get_sound_manager

class Elevator:
    """Elevator entity that players control."""
    
    def __init__(self, x, y):
        """Initialize the elevator.
        
        Args:
            x: Starting x position
            y: Starting y position
        """
        self.x = x
        self.y = y
        self.width = ELEVATOR_WIDTH
        self.height = ELEVATOR_HEIGHT
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Movement
        self.velocity_y = 0
        self.target_floor = 0
        self.current_floor = 0
        self.moving = False
        self.acceleration = ELEVATOR_ACCELERATION
        self.max_speed = ELEVATOR_SPEED
        
        # Doors
        self.doors_open = False
        self.door_position = 0  # 0 = closed, 1 = fully open
        self.door_timer = 0
        
        # Passengers
        self.passengers = []
        self.capacity = ELEVATOR_MAX_CAPACITY
        
        # Visual effects
        self.shake_amount = 0
        self.cable_tension = 0
        self.emergency_mode = False
        
        # Sound manager
        self.sound_manager = get_sound_manager()
        
        # Sound flags
        self.movement_sound_playing = False
        self.door_sound_playing = False
        
    def update(self, dt):
        """Update elevator state.
        
        Args:
            dt: Delta time in seconds
        """
        # Update movement
        if self.moving:
            self._update_movement(dt)
            
        # Update doors
        if self.doors_open:
            if self.door_position < 1.0:
                self.door_position = min(1.0, self.door_position + dt * 2)
        else:
            if self.door_position > 0:
                self.door_position = max(0, self.door_position - dt * 2)
                
        # Update shake effect (for dramatic moments)
        if self.shake_amount > 0:
            self.shake_amount = max(0, self.shake_amount - dt * 10)
            
        # Update rect position
        self.rect.x = self.x + (pygame.math.Vector2(1, 0).rotate(self.shake_amount * 100).x * 2 if self.shake_amount > 0 else 0)
        self.rect.y = self.y
        
    def _update_movement(self, dt):
        """Update elevator movement between floors."""
        if not self.moving:
            return
            
        target_y = self._get_floor_y(self.target_floor)
        distance = target_y - self.y
        
        # Debug output
        if random.random() < 0.01:  # Print occasionally to avoid spam
            print(f"Moving: current_y={self.y:.1f}, target_y={target_y:.1f}, distance={distance:.1f}")
        
        if abs(distance) > 2:  # Not at target floor yet
            # Simple movement towards target
            speed = self.max_speed * dt
            
            if distance > 0:  # Need to move down (positive y is down)
                self.y = min(target_y, self.y + speed)
            else:  # Need to move up (negative distance)
                self.y = max(target_y, self.y - speed)
            
            # Update cable tension visual
            self.cable_tension = 0.5
        else:
            # Arrived at floor
            self.y = target_y
            self.velocity_y = 0
            self.moving = False
            self.current_floor = self.target_floor
            self.cable_tension = 0
            self.sound_manager.play_sfx('elevator_arrive')
            print(f"Arrived at floor {self.current_floor}, y position: {self.y}")
            
    def move_to_floor(self, floor_number):
        """Command elevator to move to a specific floor.
        
        Args:
            floor_number: Target floor number
        """
        if floor_number in FLOORS and not self.doors_open:
            if floor_number == self.current_floor:
                print(f"Already at floor {floor_number}")
                return
                
            self.target_floor = floor_number
            self.moving = True
            self.sound_manager.play_sfx('elevator_move')
            print(f"Starting movement from floor {self.current_floor} to floor {floor_number}")
            
            # Add shake for dramatic floors
            if floor_number == -1:  # Going to evil basement
                self.shake_amount = 5
            elif floor_number == 4:  # Going to robotics lab (Alan's command center)
                self.shake_amount = 3
            elif floor_number == 17:  # Going to secret roof rave
                self.shake_amount = 4
                
    def toggle_doors(self):
        """Toggle elevator doors open/closed."""
        if not self.moving:
            self.doors_open = not self.doors_open
            self.door_timer = 0
            if self.doors_open:
                self.sound_manager.play_sfx('door_open')
            else:
                self.sound_manager.play_sfx('door_close')
            
    def open_doors(self):
        """Open elevator doors."""
        if not self.moving:
            self.doors_open = True
            self.sound_manager.play_sfx('door_open')
            
    def close_doors(self):
        """Close elevator doors."""
        self.doors_open = False
        self.sound_manager.play_sfx('door_close')
        
    def add_passenger(self, passenger):
        """Add a passenger to the elevator.
        
        Args:
            passenger: NPC passenger to add
            
        Returns:
            bool: True if passenger was added, False if full
        """
        if len(self.passengers) < self.capacity:
            self.passengers.append(passenger)
            return True
        return False
        
    def remove_passenger(self, passenger):
        """Remove a passenger from the elevator.
        
        Args:
            passenger: NPC passenger to remove
        """
        if passenger in self.passengers:
            self.passengers.remove(passenger)
            
    def is_full(self):
        """Check if elevator is at capacity.
        
        Returns:
            bool: True if elevator is full
        """
        return len(self.passengers) >= self.capacity
        
    def _get_floor_y(self, floor_number):
        """Get the y position for a given floor.
        
        Args:
            floor_number: Floor number
            
        Returns:
            float: Y position for the floor
        """
        # Ground floor (street level) is floor 0
        # Positive floors go up, negative (basement) goes down
        # The elevator should stop AT the floor line, not in the middle of the floor
        # This means the elevator bottom should align with the floor line
        base_y = SCREEN_HEIGHT - 200  # Ground floor line position
        
        # Each floor is FLOOR_HEIGHT pixels apart
        # Going up means decreasing Y (top of screen is 0)
        # Going down (basement) means increasing Y
        # Account for floor 13 not existing
        adjusted_floor = floor_number
        if floor_number > 13:
            adjusted_floor = floor_number - 1  # Shift down by 1 to account for missing floor 13
        
        # Position elevator so its bottom edge aligns with the floor line
        # Subtract elevator height so the bottom of the elevator sits on the floor line
        return base_y - (adjusted_floor * FLOOR_HEIGHT) - self.height + 10  # +10 for slight overlap with floor
        
    def draw(self, screen):
        """Draw the elevator.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw elevator shaft cables
        cable_x1 = self.rect.centerx - 15
        cable_x2 = self.rect.centerx + 15
        
        # Draw cables with tension effect
        cable_color = CABLE_COLOR if self.cable_tension < 0.5 else RED
        cable_width = 2 + int(self.cable_tension * 2)
        
        pygame.draw.line(screen, cable_color, 
                        (cable_x1, 0), (cable_x1, self.rect.top), cable_width)
        pygame.draw.line(screen, cable_color,
                        (cable_x2, 0), (cable_x2, self.rect.top), cable_width)
        
        # Draw elevator car
        car_color = ELEVATOR_COLOR
        if self.emergency_mode:
            car_color = RED
        elif self.current_floor == 4:  # Good robot lab
            car_color = (100, 150, 200)
        elif self.current_floor == -1:  # Evil basement
            car_color = (150, 50, 50)
            
        pygame.draw.rect(screen, car_color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        # Draw doors
        if self.door_position < 1.0:
            door_width = self.width * (1 - self.door_position) / 2
            left_door = pygame.Rect(self.rect.left, self.rect.top, 
                                   door_width, self.height)
            right_door = pygame.Rect(self.rect.right - door_width, self.rect.top,
                                    door_width, self.height)
            pygame.draw.rect(screen, ELEVATOR_DOOR_COLOR, left_door)
            pygame.draw.rect(screen, ELEVATOR_DOOR_COLOR, right_door)
            pygame.draw.rect(screen, BLACK, left_door, 1)
            pygame.draw.rect(screen, BLACK, right_door, 1)
            
        # Draw capacity indicator with better visibility
        capacity_text = f"PASSENGERS: {len(self.passengers)}/{self.capacity}"
        font_large = pygame.font.Font(None, 24)
        font_small = pygame.font.Font(None, 20)
        
        # Draw background for capacity
        capacity_surface = font_large.render(capacity_text, True, WHITE)
        capacity_rect = capacity_surface.get_rect(center=(self.rect.centerx, self.rect.top - 15))
        bg_rect = capacity_rect.inflate(10, 4)
        pygame.draw.rect(screen, BLACK, bg_rect)
        pygame.draw.rect(screen, GREEN if len(self.passengers) < self.capacity else RED, bg_rect, 2)
        screen.blit(capacity_surface, capacity_rect)
        
        # Draw passenger list inside elevator
        if len(self.passengers) > 0:
            y_offset = self.rect.top + 10
            for i, passenger in enumerate(self.passengers[:3]):  # Show first 3
                passenger_text = f"→ Floor {passenger.destination_floor}"
                text = font_small.render(passenger_text, True, CYAN)
                screen.blit(text, (self.rect.left + 5, y_offset))
                y_offset += 20
            
            if len(self.passengers) > 3:
                more_text = f"...+{len(self.passengers) - 3} more"
                text = font_small.render(more_text, True, GRAY)
                screen.blit(text, (self.rect.left + 5, y_offset))
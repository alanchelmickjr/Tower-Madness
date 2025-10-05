"""
NPC entity for Tower Madness / Elevator Operator
NPCs can be good robots, evil robots, or neutral characters
"""

import pygame
import random
from game.core.constants import *

class NPC:
    """Base NPC class for all characters in the game."""
    
    def __init__(self, x, y, npc_type="neutral"):
        """Initialize an NPC.
        
        Args:
            x: Starting x position
            y: Starting y position
            npc_type: Type of NPC ("good", "evil", "neutral")
        """
        self.x = x
        self.y = y
        self.width = NPC_WIDTH
        self.height = NPC_HEIGHT
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # NPC properties
        self.npc_type = npc_type
        self.destination_floor = self._choose_destination()
        self.current_floor = 0
        self.in_elevator = False
        self.waiting = True
        
        # Movement
        self.velocity_x = 0
        self.speed = NPC_SPEED
        self.direction = random.choice([-1, 1])
        
        # Behavior
        self.patience = random.uniform(10, 30)  # Seconds before leaving
        self.mood = "neutral"  # Can be "happy", "angry", "neutral"
        self.interaction_cooldown = 0
        
        # Visual properties
        self.color = self._get_color_by_type()
        self.animation_frame = 0
        self.animation_timer = 0
        
        # Special attributes for different types
        if npc_type == "good":
            self.healing_aura = True
            self.love_power = random.uniform(0.5, 1.0)
        elif npc_type == "evil":
            self.aggression = random.uniform(0.5, 1.0)
            self.chaos_level = random.uniform(0.3, 0.8)
        else:
            self.neutral_alignment = random.uniform(-0.2, 0.2)
            
    def _choose_destination(self):
        """Choose a destination floor based on NPC type.
        
        Returns:
            int: Destination floor number
        """
        if self.npc_type == "good":
            # Good robots prefer Floor 4 (Good Robot Lab) or roof (escape)
            return random.choice([4, 4, 4, 5])  # Weighted towards Floor 4
        elif self.npc_type == "evil":
            # Evil robots prefer basement (Fight Club)
            return random.choice([-1, -1, -1, 0])  # Weighted towards basement
        else:
            # Neutral NPCs go to random floors
            return random.choice([0, 1, 2, 3, 5])
            
    def _get_color_by_type(self):
        """Get NPC color based on type.
        
        Returns:
            tuple: RGB color
        """
        if self.npc_type == "good":
            # Blue/cyan shades for good robots
            return (0, random.randint(150, 255), random.randint(200, 255))
        elif self.npc_type == "evil":
            # Red/orange shades for evil robots
            return (random.randint(200, 255), random.randint(0, 100), 0)
        else:
            # Gray shades for neutral NPCs
            gray = random.randint(100, 200)
            return (gray, gray, gray)
            
    def update(self, dt):
        """Update NPC state.
        
        Args:
            dt: Delta time in seconds
        """
        # Update animation
        self.animation_timer += dt
        if self.animation_timer > 0.1:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4
            
        # Update interaction cooldown
        if self.interaction_cooldown > 0:
            self.interaction_cooldown -= dt
            
        # Update patience when waiting
        if self.waiting and not self.in_elevator:
            self.patience -= dt
            if self.patience <= 0:
                self.mood = "angry"
                
        # Update position if moving
        if not self.waiting and not self.in_elevator:
            self.x += self.velocity_x * dt
            
        # Update special effects based on type
        if self.npc_type == "good":
            self._update_good_effects(dt)
        elif self.npc_type == "evil":
            self._update_evil_effects(dt)
            
        # Update rect
        self.rect.x = self.x
        self.rect.y = self.y
        
    def _update_good_effects(self, dt):
        """Update effects for good robots."""
        # Healing aura pulses
        if hasattr(self, 'healing_aura'):
            self.love_power = 0.5 + 0.5 * abs(pygame.math.Vector2(1, 0).rotate(
                self.animation_timer * 100).x)
                
    def _update_evil_effects(self, dt):
        """Update effects for evil robots."""
        # Chaos increases over time when waiting
        if self.waiting and hasattr(self, 'chaos_level'):
            self.chaos_level = min(1.0, self.chaos_level + dt * 0.1)
            
    def enter_elevator(self, elevator):
        """Make NPC enter the elevator.
        
        Args:
            elevator: Elevator entity
            
        Returns:
            bool: True if successfully entered
        """
        if elevator.add_passenger(self):
            self.in_elevator = True
            self.waiting = False
            return True
        return False
        
    def exit_elevator(self, elevator):
        """Make NPC exit the elevator.
        
        Args:
            elevator: Elevator entity
        """
        elevator.remove_passenger(self)
        self.in_elevator = False
        self.waiting = False
        
    def interact_with(self, other_npc):
        """Interact with another NPC.
        
        Args:
            other_npc: Another NPC entity
        """
        if self.interaction_cooldown <= 0:
            if self.npc_type == "good" and other_npc.npc_type == "evil":
                # Good vs Evil interaction
                self.mood = "determined"
                other_npc.mood = "aggressive"
            elif self.npc_type == "evil" and other_npc.npc_type == "good":
                # Evil vs Good interaction
                self.mood = "aggressive"
                other_npc.mood = "determined"
            elif self.npc_type == other_npc.npc_type:
                # Same type interaction
                self.mood = "happy"
                other_npc.mood = "happy"
                
            self.interaction_cooldown = 2.0
            
    def draw(self, screen):
        """Draw the NPC.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw different styles based on type
        if self.npc_type == "good":
            self._draw_good_robot(screen)
        elif self.npc_type == "evil":
            self._draw_evil_robot(screen)
        else:
            self._draw_neutral_npc(screen)
            
        
        # Draw destination indicator
        font = pygame.font.Font(None, 16)
        dest_text = font.render(f"→F{self.destination_floor}", True, WHITE)
        dest_rect = dest_text.get_rect(center=(self.rect.centerx, self.rect.bottom + 10))
        screen.blit(dest_text, dest_rect)
        
        # Draw special effects
        if self.npc_type == "good" and hasattr(self, 'healing_aura'):
            # Draw healing aura
            aura_surface = pygame.Surface((self.width + 20, self.height + 20))
            aura_surface.set_alpha(int(50 * self.love_power))
            aura_surface.fill(CYAN)
            screen.blit(aura_surface, (self.rect.x - 10, self.rect.y - 10))
        elif self.npc_type == "evil" and hasattr(self, 'chaos_level'):
            # Draw chaos sparks
            if random.random() < self.chaos_level * 0.1:
                spark_x = self.rect.centerx + random.randint(-15, 15)
                spark_y = self.rect.centery + random.randint(-15, 15)
                pygame.draw.circle(screen, RED, (spark_x, spark_y), 2)
    
    def _draw_good_robot(self, screen):
        """Draw a Johnny 5-style good robot."""
        body_color = self.color
        if self.mood == "happy":
            body_color = tuple(min(255, c + 50) for c in self.color)
            
        # Draw treads/base (Johnny 5 style)
        tread_rect = pygame.Rect(self.rect.x, self.rect.bottom - 8, self.rect.width, 8)
        pygame.draw.rect(screen, DARK_GRAY, tread_rect)
        pygame.draw.rect(screen, BLACK, tread_rect, 1)
        
        # Draw main body (boxy robot style)
        body_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 5, self.rect.width - 4, self.rect.height - 13)
        pygame.draw.rect(screen, body_color, body_rect)
        pygame.draw.rect(screen, BLACK, body_rect, 1)
        
        # Draw head (smaller box on top)
        head_rect = pygame.Rect(self.rect.x + 8, self.rect.y, self.rect.width - 16, 12)
        pygame.draw.rect(screen, body_color, head_rect)
        pygame.draw.rect(screen, BLACK, head_rect, 1)
        
        # Draw big friendly eyes (Johnny 5 style)
        eye_y = self.rect.top + 6
        left_eye = pygame.Rect(self.rect.left + 10, eye_y - 2, 6, 6)
        right_eye = pygame.Rect(self.rect.right - 16, eye_y - 2, 6, 6)
        
        pygame.draw.ellipse(screen, WHITE, left_eye)
        pygame.draw.ellipse(screen, WHITE, right_eye)
        pygame.draw.circle(screen, BLACK, (left_eye.centerx, left_eye.centery), 2)
        pygame.draw.circle(screen, BLACK, (right_eye.centerx, right_eye.centery), 2)
        
        # Draw antenna
        pygame.draw.line(screen, GRAY, (self.rect.centerx, self.rect.top),
                        (self.rect.centerx, self.rect.top - 5), 2)
        pygame.draw.circle(screen, CYAN, (self.rect.centerx, self.rect.top - 5), 2)
        
        # Draw heart symbol on chest
        heart_x = self.rect.centerx
        heart_y = self.rect.centery
        pygame.draw.circle(screen, CYAN, (heart_x - 2, heart_y), 2)
        pygame.draw.circle(screen, CYAN, (heart_x + 2, heart_y), 2)
        pygame.draw.polygon(screen, CYAN, [
            (heart_x - 4, heart_y),
            (heart_x + 4, heart_y),
            (heart_x, heart_y + 4)
        ])
        
        # Draw healing aura
        if hasattr(self, 'healing_aura'):
            aura_surface = pygame.Surface((self.width + 20, self.height + 20))
            aura_surface.set_alpha(int(30 * self.love_power))
            aura_surface.fill(CYAN)
            screen.blit(aura_surface, (self.rect.x - 10, self.rect.y - 10))
            
    def _draw_evil_robot(self, screen):
        """Draw a humanoid evil robot."""
        body_color = self.color
        if self.mood == "angry":
            body_color = (min(255, self.color[0] + 100),
                         self.color[1] // 2,
                         self.color[2] // 2)
            
        # Draw legs (humanoid)
        leg_width = 8
        left_leg = pygame.Rect(self.rect.x + 5, self.rect.centery + 5,
                              leg_width, self.rect.height // 2 - 5)
        right_leg = pygame.Rect(self.rect.right - 13, self.rect.centery + 5,
                               leg_width, self.rect.height // 2 - 5)
        pygame.draw.rect(screen, body_color, left_leg)
        pygame.draw.rect(screen, body_color, right_leg)
        
        # Draw torso
        torso_rect = pygame.Rect(self.rect.x + 3, self.rect.y + 10,
                                 self.rect.width - 6, self.rect.height // 2)
        pygame.draw.rect(screen, body_color, torso_rect)
        pygame.draw.rect(screen, BLACK, torso_rect, 1)
        
        # Draw arms
        arm_width = 6
        left_arm = pygame.Rect(self.rect.x - 2, self.rect.y + 12,
                              arm_width, self.rect.height // 2 - 5)
        right_arm = pygame.Rect(self.rect.right - 4, self.rect.y + 12,
                               arm_width, self.rect.height // 2 - 5)
        pygame.draw.rect(screen, body_color, left_arm)
        pygame.draw.rect(screen, body_color, right_arm)
        
        # Draw head
        head_rect = pygame.Rect(self.rect.x + 7, self.rect.y,
                               self.rect.width - 14, 12)
        pygame.draw.rect(screen, body_color, head_rect)
        pygame.draw.rect(screen, BLACK, head_rect, 1)
        
        # Draw evil red eyes
        eye_y = self.rect.top + 5
        left_eye = (self.rect.left + 10, eye_y)
        right_eye = (self.rect.right - 10, eye_y)
        
        pygame.draw.circle(screen, RED, left_eye, 3)
        pygame.draw.circle(screen, RED, right_eye, 3)
        pygame.draw.circle(screen, (150, 0, 0), left_eye, 1)
        pygame.draw.circle(screen, (150, 0, 0), right_eye, 1)
        
        # Draw horns
        pygame.draw.lines(screen, RED, False, [
            (self.rect.left + 8, self.rect.top),
            (self.rect.left + 10, self.rect.top - 4),
            (self.rect.left + 12, self.rect.top)
        ], 2)
        pygame.draw.lines(screen, RED, False, [
            (self.rect.right - 12, self.rect.top),
            (self.rect.right - 10, self.rect.top - 4),
            (self.rect.right - 8, self.rect.top)
        ], 2)
        
        # Draw chaos sparks
        if hasattr(self, 'chaos_level') and random.random() < self.chaos_level * 0.1:
            spark_x = self.rect.centerx + random.randint(-15, 15)
            spark_y = self.rect.centery + random.randint(-15, 15)
            pygame.draw.circle(screen, RED, (spark_x, spark_y), 2)
            
    def _draw_neutral_npc(self, screen):
        """Draw a neutral NPC."""
        body_color = self.color
        if self.mood == "happy":
            body_color = tuple(min(255, c + 50) for c in self.color)
        elif self.mood == "angry":
            body_color = (min(255, self.color[0] + 50),
                         self.color[1] // 2,
                         self.color[2] // 2)
            
        # Simple rectangular body
        pygame.draw.rect(screen, body_color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 1)
        
        # Draw simple eyes
        eye_y = self.rect.top + 10
        left_eye = (self.rect.left + 8, eye_y)
        right_eye = (self.rect.right - 8, eye_y)
        
        pygame.draw.circle(screen, WHITE, left_eye, 3)
        pygame.draw.circle(screen, WHITE, right_eye, 3)
        pygame.draw.circle(screen, BLACK, left_eye, 1)
        pygame.draw.circle(screen, BLACK, right_eye, 1)


class GoodRobot(NPC):
    """Good robot NPC that spreads love and counters evil."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "good")
        self.love_charges = 3
        self.protection_field = True
        
    def spread_love(self, target):
        """Spread love to convert or calm other NPCs."""
        if self.love_charges > 0:
            self.love_charges -= 1
            if target.npc_type == "evil":
                # Try to convert evil robot
                if random.random() < 0.3:
                    target.npc_type = "neutral"
                    target.color = (150, 150, 150)
            elif target.npc_type == "neutral":
                # Make neutral NPC happy
                target.mood = "happy"


class EvilRobot(NPC):
    """Evil robot NPC from the basement fight club."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "evil")
        self.fight_wins = 0
        self.rage_mode = False
        
    def enter_rage_mode(self):
        """Enter rage mode after winning fights."""
        self.rage_mode = True
        self.speed *= 1.5
        self.aggression = 1.0
        
    def challenge_to_fight(self, target):
        """Challenge another NPC to fight."""
        if target.npc_type == "evil":
            # Fight between evil robots
            if random.random() < self.aggression:
                self.fight_wins += 1
                if self.fight_wins >= 3:
                    self.enter_rage_mode()
        elif target.npc_type == "good":
            # Battle between good and evil
            if random.random() < 0.5:
                # Evil wins
                target.mood = "sad"
            else:
                # Good wins
                self.mood = "defeated"
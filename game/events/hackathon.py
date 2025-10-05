"""
Hackathon event for Floor 2 - The Spaceship
Creates massive elevator traffic and chaos
"""

import pygame
import random
import math
from game.core.constants import *

class HackathonEvent:
    """Special hackathon event on Floor 2 that jams the elevator."""
    
    def __init__(self):
        """Initialize the hackathon event."""
        self.active = False
        self.timer = 0
        self.duration = 30.0  # 30 second hackathon rush (more reasonable)
        self.spawn_rate = 0.5  # Spawn hackers every 0.5 seconds
        self.spawn_timer = 0
        self.total_hackers = 0
        self.hackers_delivered = 0
        
        # Visual effects
        self.announcement_timer = 0
        self.flash_timer = 0
        self.excitement_level = 0
        
        # Special messages
        self.messages = [
            "🚨 HACKATHON STARTING ON FLOOR 2! 🚨",
            "💻 HUNDREDS OF DEVELOPERS INCOMING! 💻",
            "⚠️ ELEVATOR OVERLOAD WARNING! ⚠️",
            "🎮 THIS GAME IS BEING PLAYED HERE! 🎮",
            "🏆 SF TECH WEEK ALGORAVE HACKATHON! 🏆"
        ]
        self.current_message = 0
        self.message_timer = 0
        
        # Meta reference - the game being played at the hackathon
        self.meta_messages = [
            "Wait... is this game about THIS hackathon?",
            "They're playing Tower Madness AT the hackathon!",
            "Meta level: MAXIMUM",
            "The players are IN the game they're playing!"
        ]
        self.show_meta = False
        self.meta_timer = 0
        
    def trigger(self):
        """Trigger the hackathon event."""
        self.active = True
        self.timer = 0
        self.announcement_timer = 5.0
        self.flash_timer = 1.0
        self.excitement_level = 100
        self.total_hackers = 0
        self.hackers_delivered = 0
        print("HACKATHON EVENT TRIGGERED ON FLOOR 2!")
        
    def update(self, dt, elevator, npcs, floors):
        """Update hackathon event.
        
        Args:
            dt: Delta time
            elevator: Elevator entity
            npcs: List of NPCs
            floors: Dictionary of floors
        """
        if not self.active:
            # Random chance to trigger hackathon
            if random.random() < 0.0002:  # Rare but more common than flood
                self.trigger()
            return
            
        self.timer += dt
        
        # Update announcement
        if self.announcement_timer > 0:
            self.announcement_timer -= dt
            self.message_timer += dt
            if self.message_timer > 1.5:
                self.message_timer = 0
                self.current_message = (self.current_message + 1) % len(self.messages)
                
        # Spawn hackers at Floor 2
        if self.timer < self.duration:
            self.spawn_timer += dt
            if self.spawn_timer > self.spawn_rate:
                self.spawn_timer = 0
                self._spawn_hacker(npcs, floors)
                
        # Check for meta moment
        if self.total_hackers > 20 and not self.show_meta:
            self.show_meta = True
            self.meta_timer = 10.0
            
        if self.meta_timer > 0:
            self.meta_timer -= dt
            
        # Update visual effects
        if self.flash_timer > 0:
            self.flash_timer -= dt
            
        self.excitement_level = max(0, self.excitement_level - dt * 10)
        
        # End event after duration
        if self.timer > self.duration + 10:
            self.active = False
            print(f"Hackathon ended! Delivered {self.hackers_delivered} hackers!")
            
    def _spawn_hacker(self, npcs, floors):
        """Spawn a hacker NPC at Floor 2."""
        if 2 not in floors:
            return
            
        floor = floors[2]
        
        # Create a hacker NPC (special type)
        from game.entities.npc import NPC
        
        x = random.randint(100, SCREEN_WIDTH - 100)
        y = floor.y - 40  # NPC height
        
        hacker = NPC(x, y, "neutral")
        hacker.name = f"Hacker{self.total_hackers}"
        hacker.current_floor = 2
        
        # Hackers want to go to different floors to test the game
        possible_floors = [-1, 0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17]
        hacker.destination_floor = random.choice(possible_floors)
        
        # Hackers are impatient (they're in a hackathon!)
        hacker.patience = random.uniform(15, 25)
        
        # Special hacker colors
        hacker.color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
        
        # Add to NPCs and floor
        npcs.append(hacker)
        floor.add_waiting_npc(hacker)
        
        self.total_hackers += 1
        self.excitement_level = min(100, self.excitement_level + 10)
        
        # Sometimes spawn special developer NPCs
        if random.random() < 0.1:
            hacker.name = random.choice([
                "CoffeeDev", "BugHunter", "CodeNinja", 
                "StackOverflower", "GitMaster", "ReactLord"
            ])
            hacker.color = (0, 255, 0)  # Green for elite hackers
            
    def draw(self, screen):
        """Draw hackathon event effects.
        
        Args:
            screen: Pygame surface
        """
        if not self.active:
            return
            
        # Draw announcement
        if self.announcement_timer > 0:
            # Flashing background
            if int(self.timer * 8) % 2 == 0:
                flash_surface = pygame.Surface((SCREEN_WIDTH, 150))
                flash_surface.set_alpha(50)
                flash_surface.fill((0, 100, 255))
                screen.blit(flash_surface, (0, 50))
                
            # Draw message
            font = pygame.font.Font(None, 36)
            message = self.messages[self.current_message]
            
            # Rainbow text effect for hackathon
            colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), 
                     (0, 255, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]
            color_index = int(self.timer * 10) % len(colors)
            
            text = font.render(message, True, colors[color_index])
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            
            # Background
            bg_rect = text_rect.inflate(20, 10)
            pygame.draw.rect(screen, (0, 0, 0), bg_rect)
            pygame.draw.rect(screen, colors[color_index], bg_rect, 2)
            
            screen.blit(text, text_rect)
            
        # Draw meta messages
        if self.show_meta and self.meta_timer > 0:
            meta_font = pygame.font.Font(None, 28)
            meta_index = int(self.meta_timer * 0.5) % len(self.meta_messages)
            meta_text = self.meta_messages[meta_index]
            
            # Glitch effect for meta moment
            for i in range(3):
                offset_x = random.randint(-2, 2)
                offset_y = random.randint(-2, 2)
                color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
                glitch_text = meta_font.render(meta_text, True, color)
                glitch_rect = glitch_text.get_rect(center=(SCREEN_WIDTH // 2 + offset_x, 200 + offset_y))
                glitch_text.set_alpha(100)
                screen.blit(glitch_text, glitch_rect)
                
            # Main text
            main_text = meta_font.render(meta_text, True, WHITE)
            main_rect = main_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
            screen.blit(main_text, main_rect)
            
        # Draw stats
        if self.timer < self.duration:
            stats_font = pygame.font.Font(None, 24)
            
            # Hacker count
            count_text = stats_font.render(f"Hackers spawned: {self.total_hackers}", True, CYAN)
            screen.blit(count_text, (20, 180))
            
            # Time remaining
            time_left = max(0, self.duration - self.timer)
            time_text = stats_font.render(f"Hackathon time: {time_left:.1f}s", True, YELLOW)
            screen.blit(time_text, (20, 200))
            
            # Excitement meter
            self._draw_excitement_meter(screen, 20, 220)
            
        # Draw "FLOOR 2 - HACKATHON IN PROGRESS" on the floor
        if self.active and self.timer < self.duration:
            floor_font = pygame.font.Font(None, 20)
            floor_text = floor_font.render("FLOOR 2: HACKATHON IN PROGRESS!", True, 
                                          (255, 0, 0) if int(self.timer * 4) % 2 == 0 else (255, 255, 0))
            floor_rect = floor_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
            screen.blit(floor_text, floor_rect)
            
    def _draw_excitement_meter(self, screen, x, y):
        """Draw the excitement level meter."""
        font = pygame.font.Font(None, 20)
        label = font.render("CHAOS LEVEL", True, WHITE)
        screen.blit(label, (x, y))
        
        # Bar background
        bar_rect = pygame.Rect(x + 100, y, 150, 20)
        pygame.draw.rect(screen, DARK_GRAY, bar_rect)
        
        # Bar fill (rainbow for hackathon!)
        fill_width = int((self.excitement_level / 100) * 150)
        if fill_width > 0:
            for i in range(fill_width):
                color_index = (i + int(self.timer * 50)) % 7
                colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), 
                         (0, 255, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]
                pygame.draw.rect(screen, colors[color_index], (x + 100 + i, y, 1, 20))
                
        # Bar border
        pygame.draw.rect(screen, WHITE, bar_rect, 1)
        
    def check_elevator_at_floor_2(self, elevator):
        """Check if elevator is at Floor 2 during hackathon.
        
        Returns:
            bool: True if at Floor 2 during active hackathon
        """
        return self.active and elevator.current_floor == 2 and self.timer < self.duration
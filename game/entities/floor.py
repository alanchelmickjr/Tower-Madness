"""
Floor entity for Tower Madness / Elevator Operator
Each floor has its own personality and narrative purpose
"""

import pygame
import random
from game.core.constants import *

class Floor:
    """Represents a floor in the tower with unique characteristics."""
    
    def __init__(self, floor_number, y_position):
        """Initialize a floor.
        
        Args:
            floor_number: The floor number (-1 for basement, 0 for street, etc.)
            y_position: Y position on screen
        """
        self.floor_number = floor_number
        self.y = y_position
        self.floor_data = FLOORS.get(floor_number, {
            "name": f"Floor {floor_number}",
            "description": "Unknown floor",
            "theme": "neutral",
            "color": GRAY,
            "ambient_color": (150, 150, 150)
        })
        
        # Visual properties
        self.width = SCREEN_WIDTH
        self.height = FLOOR_HEIGHT
        self.rect = pygame.Rect(0, y_position, self.width, 10)
        
        # NPCs waiting at this floor
        self.waiting_npcs = []
        self.max_waiting = 8
        
        # Special floor effects
        self.effect_timer = 0
        self.glow_intensity = 0
        
        # Floor-specific attributes
        self.is_good_robot_lab = (floor_number == 4)  # Alan's command center
        self.is_evil_fight_club = (floor_number == -1)
        self.is_street_level = (floor_number == 0)  # John the doorman
        self.is_roof_rave = (floor_number == 17)  # Secret rave venue
        self.is_event_space = (floor_number == 2)  # The Spaceship
        self.is_gym = (floor_number == 5)  # Under construction
        self.is_arts_music = (floor_number == 6)
        self.is_biotech = (floor_number == 8)
        self.is_ai_lab = (floor_number == 9)
        self.is_vc_floor = (floor_number == 10)
        self.is_crypto = (floor_number == 12)
        self.is_dacc_lounge = (floor_number == 16)
        
        # Ambient animations
        self.ambient_particles = []
        self.light_flicker = 0
        
    def update(self, dt):
        """Update floor state and effects.
        
        Args:
            dt: Delta time in seconds
        """
        self.effect_timer += dt
        
        # Update special floor effects
        if self.is_good_robot_lab:
            self._update_good_lab_effects(dt)
        elif self.is_evil_fight_club:
            self._update_evil_basement_effects(dt)
        elif self.is_roof_rave:
            self._update_roof_rave_effects(dt)
        elif self.is_event_space:
            self._update_event_space_effects(dt)
        elif self.is_crypto:
            self._update_crypto_effects(dt)
        elif self.is_dacc_lounge:
            self._update_dacc_lounge_effects(dt)
            
        # Update ambient particles
        self._update_particles(dt)
        
        # Update NPCs waiting
        for npc in self.waiting_npcs[:]:
            if hasattr(npc, 'patience'):
                npc.patience -= dt
                if npc.patience <= 0:
                    self.waiting_npcs.remove(npc)
                    
    def _update_good_lab_effects(self, dt):
        """Update effects for the good robot lab on Floor 4."""
        # Gentle pulsing blue glow
        self.glow_intensity = abs(pygame.math.Vector2(1, 0).rotate(
            self.effect_timer * 50).x) * 0.5 + 0.5
            
        # Create healing/love particles
        if random.random() < 0.1:
            self.ambient_particles.append({
                'x': random.randint(100, SCREEN_WIDTH - 100),
                'y': self.y,
                'vx': random.uniform(-20, 20),
                'vy': random.uniform(-30, -10),
                'life': 2.0,
                'color': CYAN,
                'type': 'heart'
            })
            
    def _update_evil_basement_effects(self, dt):
        """Update effects for the evil robot fight club basement."""
        # Aggressive red flashing
        self.light_flicker = random.random() * 0.3 + 0.7
        
        # Create sparks and smoke particles
        if random.random() < 0.2:
            self.ambient_particles.append({
                'x': random.randint(100, SCREEN_WIDTH - 100),
                'y': self.y,
                'vx': random.uniform(-50, 50),
                'vy': random.uniform(-20, 20),
                'life': 1.0,
                'color': RED,
                'type': 'spark'
            })
            
    def _update_roof_rave_effects(self, dt):
        """Update effects for the roof rave (escape destination)."""
        # Rainbow disco effects
        self.glow_intensity = abs(pygame.math.Vector2(1, 0).rotate(
            self.effect_timer * 200).x)
            
        # Create party particles
        if random.random() < 0.15:
            colors = [CYAN, MAGENTA, YELLOW, GREEN]
            self.ambient_particles.append({
                'x': random.randint(100, SCREEN_WIDTH - 100),
                'y': self.y,
                'vx': random.uniform(-30, 30),
                'vy': random.uniform(-50, -20),
                'life': 1.5,
                'color': random.choice(colors),
                'type': 'confetti'
            })
            
    def _update_event_space_effects(self, dt):
        """Update effects for The Spaceship event space."""
        # Gentle blue pulsing for spaceship theme
        self.glow_intensity = abs(pygame.math.Vector2(1, 0).rotate(
            self.effect_timer * 30).x) * 0.3 + 0.7
            
        # Create star particles
        if random.random() < 0.05:
            self.ambient_particles.append({
                'x': random.randint(100, SCREEN_WIDTH - 100),
                'y': self.y,
                'vx': random.uniform(-10, 10),
                'vy': random.uniform(-20, -5),
                'life': 3.0,
                'color': WHITE,
                'type': 'star'
            })
            
    def _update_crypto_effects(self, dt):
        """Update effects for Crypto/DeFi floor."""
        # Orange bitcoin glow
        self.glow_intensity = abs(pygame.math.Vector2(1, 0).rotate(
            self.effect_timer * 100).x) * 0.4 + 0.6
            
        # Create bitcoin/coin particles
        if random.random() < 0.08:
            self.ambient_particles.append({
                'x': random.randint(100, SCREEN_WIDTH - 100),
                'y': self.y - 20,
                'vx': 0,
                'vy': random.uniform(10, 30),
                'life': 2.0,
                'color': GOLD,
                'type': 'coin'
            })
            
    def _update_dacc_lounge_effects(self, dt):
        """Update effects for d/acc Lounge."""
        # Magenta acceleration waves
        self.glow_intensity = abs(pygame.math.Vector2(1, 0).rotate(
            self.effect_timer * 150).x)
            
        # Create acceleration particles
        if random.random() < 0.1:
            self.ambient_particles.append({
                'x': random.randint(100, SCREEN_WIDTH - 100),
                'y': self.y,
                'vx': random.uniform(-40, 40),
                'vy': random.uniform(-40, -20),
                'life': 1.5,
                'color': MAGENTA,
                'type': 'acceleration'
            })
            
    def _update_particles(self, dt):
        """Update ambient particle effects."""
        for particle in self.ambient_particles[:]:
            particle['life'] -= dt
            if particle['life'] <= 0:
                self.ambient_particles.remove(particle)
            else:
                particle['x'] += particle['vx'] * dt
                particle['y'] += particle['vy'] * dt
                particle['vy'] += 50 * dt  # Gravity
                
    def add_waiting_npc(self, npc):
        """Add an NPC to the waiting queue.
        
        Args:
            npc: NPC entity to add
            
        Returns:
            bool: True if added, False if floor is full
        """
        if len(self.waiting_npcs) < self.max_waiting:
            self.waiting_npcs.append(npc)
            return True
        return False
        
    def remove_waiting_npc(self, npc):
        """Remove an NPC from the waiting queue.
        
        Args:
            npc: NPC entity to remove
        """
        if npc in self.waiting_npcs:
            self.waiting_npcs.remove(npc)
            
    def draw(self, screen):
        """Draw the floor and its effects.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw floor platform
        floor_color = self.floor_data["color"]
        
        # Apply special effects to color
        if self.is_evil_fight_club:
            # Red flashing for fight club
            r = min(255, floor_color[0] + int(100 * self.light_flicker))
            floor_color = (r, 0, 0)
        elif self.is_good_robot_lab:
            # Blue glow for good lab
            b = min(255, floor_color[2] + int(100 * self.glow_intensity))
            floor_color = (0, 100, b)
            
        # Main floor platform
        platform_rect = pygame.Rect(0, self.y, SCREEN_WIDTH, 5)
        pygame.draw.rect(screen, floor_color, platform_rect)
        
        # Draw floor details
        self._draw_floor_details(screen)
        
        # Draw ambient particles
        for particle in self.ambient_particles:
            alpha = particle['life'] / 2.0
            color = (*particle['color'], int(255 * alpha))
            
            if particle['type'] == 'heart':
                # Draw heart shape for good lab
                self._draw_heart(screen, particle['x'], particle['y'], 8, particle['color'])
            elif particle['type'] == 'spark':
                # Draw spark for fight club
                pygame.draw.circle(screen, particle['color'], 
                                 (int(particle['x']), int(particle['y'])), 3)
            elif particle['type'] == 'confetti':
                # Draw confetti for roof rave
                pygame.draw.rect(screen, particle['color'],
                                (particle['x'], particle['y'], 5, 5))
            elif particle['type'] == 'star':
                # Draw star for event space
                pygame.draw.circle(screen, particle['color'],
                                 (int(particle['x']), int(particle['y'])), 2)
            elif particle['type'] == 'coin':
                # Draw coin for crypto floor
                pygame.draw.circle(screen, GOLD,
                                 (int(particle['x']), int(particle['y'])), 4)
                pygame.draw.circle(screen, ORANGE,
                                 (int(particle['x']), int(particle['y'])), 4, 1)
            elif particle['type'] == 'acceleration':
                # Draw acceleration particle
                pygame.draw.line(screen, particle['color'],
                               (particle['x'] - 3, particle['y']),
                               (particle['x'] + 3, particle['y']), 2)
                
        # Draw special floor indicators FIRST (so regular label draws on top if needed)
        if self.is_good_robot_lab:
            # Draw protective barrier effect FIRST (so text goes on top)
            barrier_rect = pygame.Rect(0, self.y - 40, SCREEN_WIDTH, 50)
            barrier_surface = pygame.Surface((SCREEN_WIDTH, 50))
            barrier_surface.set_alpha(int(20 * self.glow_intensity))  # Very subtle
            barrier_surface.fill(CYAN)
            screen.blit(barrier_surface, barrier_rect)
            
            # Draw "GOOD" indicator with HIGH CONTRAST
            good_font = pygame.font.Font(None, 36)  # Larger font
            good_text = good_font.render("♥ GOOD ROBOTS ♥", True, YELLOW)  # YELLOW for max contrast
            good_rect = good_text.get_rect(center=(SCREEN_WIDTH // 2, self.y - 20))
            
            # Draw solid black background box
            bg_rect = good_rect.inflate(30, 15)
            pygame.draw.rect(screen, BLACK, bg_rect)
            pygame.draw.rect(screen, CYAN, bg_rect, 3)  # Thicker cyan border
            
            screen.blit(good_text, good_rect)
        
        # Draw floor label (after special indicators)
        font = pygame.font.Font(None, 24)
        label = font.render(self.floor_data["name"], True, WHITE)
        label_rect = label.get_rect(midleft=(20, self.y - 15))
        screen.blit(label, label_rect)
            
        # Draw other special floor indicators
        if self.is_evil_fight_club:
            # Draw "EVIL" indicator with warning
            evil_font = pygame.font.Font(None, 32)
            evil_text = evil_font.render("⚠ ROBOT FIGHT CLUB ⚠", True, RED)
            evil_rect = evil_text.get_rect(center=(SCREEN_WIDTH // 2, self.y - 20))
            screen.blit(evil_text, evil_rect)
            
            # Draw cage/prison bars effect
            for x in range(0, SCREEN_WIDTH, 40):
                bar_rect = pygame.Rect(x, self.y - 35, 3, 35)
                pygame.draw.rect(screen, (100, 0, 0), bar_rect)
                
        elif self.is_roof_rave:
            # Draw "SECRET RAVE" indicator with disco effect
            rave_font = pygame.font.Font(None, 32)
            colors = [CYAN, MAGENTA, YELLOW, GREEN]
            color_index = int(self.effect_timer * 4) % len(colors)
            rave_text = rave_font.render("🎉 SECRET RAVE 🎉", True, colors[color_index])
            rave_rect = rave_text.get_rect(center=(SCREEN_WIDTH // 2, self.y - 20))
            screen.blit(rave_text, rave_rect)
            
        elif self.is_gym:
            # Draw "UNDER CONSTRUCTION" sign
            construction_font = pygame.font.Font(None, 24)
            construction_text = construction_font.render("🚧 UNDER CONSTRUCTION 🚧", True, ORANGE)
            construction_rect = construction_text.get_rect(center=(SCREEN_WIDTH // 2, self.y - 20))
            screen.blit(construction_text, construction_rect)
                
        # Draw waiting NPCs count
        if self.waiting_npcs:
            count_text = font.render(f"Waiting: {len(self.waiting_npcs)}", True, YELLOW)
            count_rect = count_text.get_rect(midright=(SCREEN_WIDTH - 20, self.y - 15))
            screen.blit(count_text, count_rect)
            
    def _draw_floor_details(self, screen):
        """Draw additional floor-specific details."""
        if self.is_street_level:
            # Draw entrance/exit indicators
            font = pygame.font.Font(None, 20)
            entrance_text = font.render("← EXIT", True, GREEN)
            screen.blit(entrance_text, (10, self.y + 10))
            entrance_text2 = font.render("ENTER →", True, GREEN)
            screen.blit(entrance_text2, (SCREEN_WIDTH - 70, self.y + 10))
            
    def _draw_heart(self, screen, x, y, size, color):
        """Draw a heart shape for good robot effects.
        
        Args:
            screen: Pygame surface
            x, y: Position
            size: Size of the heart
            color: Color tuple
        """
        # Simple heart using circles and polygon
        pygame.draw.circle(screen, color, (x - size//2, y), size//2)
        pygame.draw.circle(screen, color, (x + size//2, y), size//2)
        pygame.draw.polygon(screen, color, [
            (x - size, y),
            (x + size, y),
            (x, y + size)
        ])
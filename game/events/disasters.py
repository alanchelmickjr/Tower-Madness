"""
Disaster events for Tower Madness
Including the epic flood event and other emergencies
"""

import pygame
import random
import math
from game.core.constants import *

class FloodDisaster:
    """Epic flood disaster that threatens the tower."""
    
    def __init__(self):
        """Initialize the flood disaster."""
        self.active = False
        self.water_level = SCREEN_HEIGHT + 100  # Start below screen
        self.target_water_level = SCREEN_HEIGHT + 100
        self.flood_speed = 50  # Pixels per second rising
        self.flood_timer = 0
        self.warning_timer = 0
        self.warning_phase = False
        self.crisis_phase = False
        self.resolution_phase = False
        self.max_duration = 45.0  # Maximum 45 seconds before auto-resolve
        
        # Visual effects
        self.water_color = (50, 100, 200, 180)  # Semi-transparent blue
        self.foam_particles = []
        self.debris_objects = []
        self.lightning_flash = 0
        self.screen_shake = 0
        self.shake_timer = 0  # Timer for periodic shake pulses
        self.shake_pulse_interval = 3.0  # Shake every 3 seconds
        
        # Flood stages
        self.flood_stage = 0  # 0: calm, 1: warning, 2: rising, 3: peak, 4: receding
        self.stage_messages = [
            "The basement pipes are making strange noises...",
            "⚠️ FLOOD WARNING! Water detected in basement! ⚠️",
            "💧 WATER RISING RAPIDLY! EVACUATE LOWER FLOORS! 💧",
            "🌊 CATASTROPHIC FLOODING! SEEK HIGHER GROUND! 🌊",
            "Water levels receding... Crisis averted!"
        ]
        
        # Heroes who can help
        self.heroes_spawned = False
        self.xeno_helping = False
        self.james_helping = False
        
    def trigger_flood(self):
        """Trigger the flood disaster event."""
        self.active = True
        self.flood_stage = 1
        self.warning_phase = True
        self.warning_timer = 5.0  # 5 seconds warning
        self.screen_shake = 10
        print("FLOOD DISASTER TRIGGERED!")
        
    def update(self, dt, elevator, npcs):
        """Update flood disaster state.
        
        Args:
            dt: Delta time
            elevator: Elevator entity
            npcs: List of NPCs in the game
        """
        if not self.active:
            # Random chance to trigger flood (balanced frequency)
            if random.random() < 0.0001:  # Slowed down 2x
                self.trigger_flood()
            return
            
        self.flood_timer += dt
        
        # Auto-resolve after max duration
        if self.flood_timer > self.max_duration:
            self.resolution_phase = True
            self.crisis_phase = False
            self.warning_phase = False
            self.flood_stage = 4
            self.target_water_level = SCREEN_HEIGHT + 100
        
        # Update flood stages
        if self.warning_phase:
            self.warning_timer -= dt
            if self.warning_timer <= 0:
                self.warning_phase = False
                self.crisis_phase = True
                self.flood_stage = 2
                self.target_water_level = SCREEN_HEIGHT - 200  # Flood to floor 2
                
        elif self.crisis_phase:
            # Water rising
            if self.water_level > self.target_water_level:
                self.water_level -= self.flood_speed * dt
                
                # Check if peak reached
                if self.water_level <= self.target_water_level:
                    self.flood_stage = 3
                    # Spawn heroes if not already
                    if not self.heroes_spawned:
                        self._spawn_heroes(npcs)
                        
            # Check for hero intervention
            if self.xeno_helping and self.james_helping:
                # Both heroes helping - start receding
                self.resolution_phase = True
                self.crisis_phase = False
                self.flood_stage = 4
                self.target_water_level = SCREEN_HEIGHT + 100
                
        elif self.resolution_phase:
            # Water receding
            if self.water_level < self.target_water_level:
                self.water_level += self.flood_speed * 2 * dt  # Recede faster
                
                if self.water_level >= self.target_water_level:
                    # Flood ended
                    self.active = False
                    self.flood_stage = 0
                    self.reset()
                    
        # Update visual effects
        self._update_effects(dt)
        
        # Check elevator safety
        if elevator.y + elevator.height > self.water_level:
            # Elevator in water - emergency mode
            elevator.emergency_mode = True
            if elevator.current_floor < 3:
                # Force elevator up
                elevator.move_to_floor(3)
                
        # Update NPCs in flood
        for npc in npcs:
            if npc.y + npc.height > self.water_level:
                # NPC in water - make them panic
                npc.patience = max(5, npc.patience)
                npc.mood = "panicked"
                # Move them toward elevator
                if not npc.in_elevator:
                    if npc.x < elevator.x:
                        npc.x += npc.speed * 2 * dt
                    else:
                        npc.x -= npc.speed * 2 * dt
                        
    def _spawn_heroes(self, npcs):
        """Spawn Xeno and Headphone James to save the day."""
        self.heroes_spawned = True
        # Heroes will be spawned by the scene manager
        # This just sets the flag
        
    def _update_effects(self, dt):
        """Update visual effects for the flood."""
        # Periodic screen shake pulse during crisis (not continuous)
        if self.crisis_phase:
            self.shake_timer += dt
            
            # Pulse shake every few seconds instead of continuously
            if self.shake_timer >= self.shake_pulse_interval:
                self.screen_shake = 8  # Moderate shake pulse
                self.shake_timer = 0
                
            # Quick decay after pulse
            self.screen_shake = max(0, self.screen_shake - dt * 20)
                
        # Create foam particles at water surface
        if self.active and random.random() < 0.3:
            self.foam_particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': self.water_level,
                'vx': random.uniform(-20, 20),
                'vy': random.uniform(-30, -10),
                'life': 2.0,
                'size': random.randint(2, 5)
            })
            
        # Update foam particles
        for particle in self.foam_particles[:]:
            particle['life'] -= dt
            if particle['life'] <= 0:
                self.foam_particles.remove(particle)
            else:
                particle['x'] += particle['vx'] * dt
                particle['y'] += particle['vy'] * dt
                particle['vy'] += 50 * dt  # Gravity
                
        # Create debris
        if self.crisis_phase and random.random() < 0.05:
            self.debris_objects.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': self.water_level + 20,
                'vx': random.uniform(-30, 30),
                'rotation': random.uniform(0, 360),
                'rotation_speed': random.uniform(-180, 180),
                'type': random.choice(['box', 'barrel', 'plank'])
            })
            
        # Update debris
        for debris in self.debris_objects[:]:
            debris['x'] += debris['vx'] * dt
            debris['rotation'] += debris['rotation_speed'] * dt
            # Remove if off screen
            if debris['x'] < -50 or debris['x'] > SCREEN_WIDTH + 50:
                self.debris_objects.remove(debris)
                
        # Lightning effect during peak
        if self.flood_stage == 3:
            if random.random() < 0.02:
                self.lightning_flash = 0.5
        if self.lightning_flash > 0:
            self.lightning_flash -= dt
            
    def draw(self, screen, camera_y=0):
        """Draw the flood disaster.
        
        Args:
            screen: Pygame surface
            camera_y: Camera Y offset for scrolling
        """
        if not self.active:
            return
            
        # Draw water
        water_rect = pygame.Rect(0, self.water_level + camera_y, 
                                SCREEN_WIDTH, SCREEN_HEIGHT - self.water_level)
        
        # Create water surface with transparency
        water_surface = pygame.Surface((SCREEN_WIDTH, 
                                       max(0, SCREEN_HEIGHT - self.water_level - camera_y)), 
                                      pygame.SRCALPHA)
        
        # Base water color
        water_surface.fill((50, 100, 200, 120))
        
        # Add wave effect
        wave_height = 10 + abs(math.sin(self.flood_timer * 2)) * 5
        for x in range(0, SCREEN_WIDTH, 20):
            wave_y = math.sin(x * 0.05 + self.flood_timer * 3) * wave_height
            pygame.draw.circle(water_surface, (100, 150, 255, 80), 
                             (x, int(wave_y)), 15)
            
        screen.blit(water_surface, (0, self.water_level + camera_y))
        
        # Draw foam particles
        for particle in self.foam_particles:
            alpha = int(255 * (particle['life'] / 2.0))
            pygame.draw.circle(screen, (255, 255, 255), 
                             (int(particle['x']), int(particle['y'] + camera_y)), 
                             particle['size'])
                             
        # Draw debris
        for debris in self.debris_objects:
            # Save current transform
            if debris['type'] == 'box':
                # Draw floating box
                box_rect = pygame.Rect(debris['x'] - 10, 
                                      self.water_level - 5 + camera_y, 20, 15)
                pygame.draw.rect(screen, (139, 69, 19), box_rect)
                pygame.draw.rect(screen, (0, 0, 0), box_rect, 1)
            elif debris['type'] == 'barrel':
                # Draw floating barrel
                pygame.draw.ellipse(screen, (101, 67, 33), 
                                   pygame.Rect(debris['x'] - 8, 
                                             self.water_level - 5 + camera_y, 16, 20))
            else:  # plank
                # Draw floating plank
                pygame.draw.rect(screen, (160, 82, 45), 
                               (debris['x'] - 15, self.water_level - 3 + camera_y, 30, 6))
                               
        # Draw warning text
        if self.flood_stage > 0 and self.flood_stage < 5:
            font = pygame.font.Font(None, 36)
            message = self.stage_messages[self.flood_stage - 1]
            
            # Flashing effect for warnings
            if self.flood_stage in [2, 3]:
                if int(self.flood_timer * 4) % 2 == 0:
                    color = RED
                else:
                    color = YELLOW
            else:
                color = WHITE
                
            text = font.render(message, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            
            # Background for text
            bg_rect = text_rect.inflate(20, 10)
            pygame.draw.rect(screen, (0, 0, 0, 180), bg_rect)
            pygame.draw.rect(screen, color, bg_rect, 2)
            
            screen.blit(text, text_rect)
            
        # Lightning flash effect (border only)
        if self.lightning_flash > 0:
            border = int(30 * self.lightning_flash)
            pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, border))
            pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT - border, SCREEN_WIDTH, border))
            pygame.draw.rect(screen, WHITE, (0, 0, border, SCREEN_HEIGHT))
            pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - border, 0, border, SCREEN_HEIGHT))
            
        # Draw hero arrival message
        if self.heroes_spawned and not self.resolution_phase:
            hero_font = pygame.font.Font(None, 28)
            hero_text = hero_font.render("🦸 HEROES ARRIVING TO SAVE THE DAY! 🦸", True, CYAN)
            hero_rect = hero_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
            screen.blit(hero_text, hero_rect)
            
    def reset(self):
        """Reset the flood disaster."""
        self.active = False
        self.water_level = SCREEN_HEIGHT + 100
        self.target_water_level = SCREEN_HEIGHT + 100
        self.flood_timer = 0
        self.warning_timer = 0
        self.warning_phase = False
        self.crisis_phase = False
        self.resolution_phase = False
        self.flood_stage = 0
        self.foam_particles.clear()
        self.debris_objects.clear()
        self.lightning_flash = 0
        self.screen_shake = 0
        self.shake_timer = 0
        self.heroes_spawned = False
        self.xeno_helping = False
        self.james_helping = False
        
    def get_shake_offset(self):
        """Get screen shake offset for rendering.
        
        Returns:
            Tuple of (x, y) shake offset
        """
        if self.screen_shake > 0:
            return (random.randint(-int(self.screen_shake), int(self.screen_shake)),
                   random.randint(-int(self.screen_shake), int(self.screen_shake)))
        return (0, 0)


class PowerOutage:
    """Power outage disaster - emergency lights kick in, elevator disabled."""
    
    def __init__(self):
        self.active = False
        self.timer = 0
        self.duration = 10.0
        self.flicker_timer = 0
        self.emergency_lights_on = False
        self.elevator_disabled = False
        
    def trigger(self):
        self.active = True
        self.timer = 0
        self.emergency_lights_on = True
        self.elevator_disabled = True
        print("⚡ POWER OUTAGE! Emergency lights activated. Elevator disabled.")
        
    def update(self, dt):
        if not self.active:
            if random.random() < 0.00005:  # Slowed down 2x
                self.trigger()
            return
            
        self.timer += dt
        
        if self.timer > self.duration:
            self.active = False
            self.emergency_lights_on = False
            self.elevator_disabled = False
            print("✓ Power restored. Elevator operational.")
            
    def draw(self, screen):
        if self.active:
            # Emergency lights - dim red/amber glow instead of darkness
            emergency_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            emergency_overlay.set_alpha(120)
            emergency_overlay.fill((80, 20, 0))  # Dark red-amber emergency lighting
            screen.blit(emergency_overlay, (0, 0))
            
            # Warning text
            font = pygame.font.Font(None, 36)
            text = font.render("⚡ POWER OUTAGE - EMERGENCY LIGHTS ON ⚡", True, (255, 200, 0))
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            bg_rect = rect.inflate(20, 10)
            pygame.draw.rect(screen, BLACK, bg_rect)
            pygame.draw.rect(screen, (255, 200, 0), bg_rect, 2)
            screen.blit(text, rect)
            
            # Elevator status warning
            small_font = pygame.font.Font(None, 24)
            elevator_text = small_font.render("⚠️ ELEVATOR DISABLED ⚠️", True, RED)
            elevator_rect = elevator_text.get_rect(center=(SCREEN_WIDTH // 2, 140))
            screen.blit(elevator_text, elevator_rect)


class FireAlarm:
    """Fire alarm event that requires evacuation."""
    
    def __init__(self):
        """Initialize fire alarm event."""
        self.active = False
        self.alarm_timer = 0
        self.alarm_sound = True
        
    def trigger(self):
        """Trigger the fire alarm."""
        self.active = True
        self.alarm_timer = 30.0  # 30 second evacuation
        
    def update(self, dt):
        """Update fire alarm state."""
        if self.active:
            self.alarm_timer -= dt
            self.alarm_sound = int(self.alarm_timer * 4) % 2 == 0
            
            if self.alarm_timer <= 0:
                self.active = False
                
    def draw(self, screen):
        """Draw fire alarm effects."""
        if self.active and self.alarm_sound:
            # Red flashing overlay
            alarm_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            alarm_surface.set_alpha(30)
            alarm_surface.fill((255, 0, 0))
            screen.blit(alarm_surface, (0, 0))
            
            # Alarm text
            font = pygame.font.Font(None, 48)
            text = font.render("🚨 FIRE ALARM - EVACUATE! 🚨", True, RED)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 50))
            screen.blit(text, text_rect)
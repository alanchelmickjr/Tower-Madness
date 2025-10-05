"""
Exciting intro scene for Tower Madness
Sets the stage with action and drama
"""

import pygame
import random
import math
from game.core.constants import *

class IntroScene:
    """Dramatic intro scene with action."""
    
    def __init__(self):
        """Initialize the intro scene."""
        self.timer = 0
        self.phase = 0  # 0: title, 1: story, 2: action, 3: ready
        self.phase_timer = 0
        self.complete = False
        
        # Visual effects
        self.particles = []
        self.lightning_effects = []
        self.robot_silhouettes = []
        self.text_fade = 0
        self.screen_flash = 0
        
        # Story text
        self.story_lines = [
            "FRONTIER TOWER - SAN FRANCISCO",
            "Where innovation meets chaos...",
            "",
            "Good robots build the future on Floor 4",
            "Evil robots plot destruction in the basement",
            "",
            "Between them stands YOU:",
            "THE ELEVATOR OPERATOR",
            "",
            "Can you maintain order?",
            "Can you prevent disaster?",
            "Can you... SAVE THE TOWER?"
        ]
        
        self.current_line = 0
        self.line_timer = 0
        
        # Action sequence elements
        self.explosion_timer = 0
        self.robot_battle_timer = 0
        self.elevator_shake = 0
        
        # Initialize robot positions for battle scene
        self._init_robot_battle()
        
    def _init_robot_battle(self):
        """Initialize positions for robot battle animation."""
        # Good robots on left
        for i in range(3):
            self.robot_silhouettes.append({
                'x': 100 + i * 50,
                'y': SCREEN_HEIGHT // 2 + random.randint(-50, 50),
                'vx': random.uniform(20, 40),
                'vy': random.uniform(-10, 10),
                'type': 'good',
                'color': CYAN,
                'size': 20
            })
            
        # Evil robots on right
        for i in range(3):
            self.robot_silhouettes.append({
                'x': SCREEN_WIDTH - 100 - i * 50,
                'y': SCREEN_HEIGHT // 2 + random.randint(-50, 50),
                'vx': random.uniform(-40, -20),
                'vy': random.uniform(-10, 10),
                'type': 'evil',
                'color': RED,
                'size': 20
            })
            
    def update(self, dt, events):
        """Update the intro scene.
        
        Args:
            dt: Delta time
            events: Pygame events
        """
        self.timer += dt
        self.phase_timer += dt
        
        # Check for skip
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    # Skip to next phase or end
                    if self.phase < 3:
                        self.phase += 1
                        self.phase_timer = 0
                        self.current_line = 0
                    else:
                        self.complete = True
                        
        # Update based on phase
        if self.phase == 0:
            self._update_title_phase(dt)
        elif self.phase == 1:
            self._update_story_phase(dt)
        elif self.phase == 2:
            self._update_action_phase(dt)
        elif self.phase == 3:
            self._update_ready_phase(dt)
            
        # Update visual effects
        self._update_effects(dt)
        
    def _update_title_phase(self, dt):
        """Update title animation phase."""
        # Fade in text
        self.text_fade = min(255, self.text_fade + dt * 100)
        
        # Create dramatic particles
        if random.random() < 0.1:
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': SCREEN_HEIGHT,
                'vx': random.uniform(-50, 50),
                'vy': random.uniform(-200, -100),
                'life': 3.0,
                'color': random.choice([CYAN, RED, YELLOW]),
                'size': random.randint(2, 5)
            })
            
        # Auto-advance after 3 seconds
        if self.phase_timer > 3.0:
            self.phase = 1
            self.phase_timer = 0
            
    def _update_story_phase(self, dt):
        """Update story text phase."""
        self.line_timer += dt
        
        # Show next line every 2 seconds
        if self.line_timer > 2.0:
            self.line_timer = 0
            self.current_line += 1
            
            if self.current_line >= len(self.story_lines):
                self.phase = 2
                self.phase_timer = 0
                self.screen_flash = 1.0
                
    def _update_action_phase(self, dt):
        """Update action sequence phase."""
        # Robot battle animation
        for robot in self.robot_silhouettes:
            robot['x'] += robot['vx'] * dt
            robot['y'] += robot['vy'] * dt
            
            # Bounce off edges
            if robot['x'] < 50 or robot['x'] > SCREEN_WIDTH - 50:
                robot['vx'] *= -0.8
            if robot['y'] < 100 or robot['y'] > SCREEN_HEIGHT - 100:
                robot['vy'] *= -0.8
                
            # Add some randomness
            robot['vx'] += random.uniform(-20, 20) * dt
            robot['vy'] += random.uniform(-20, 20) * dt
            
        # Explosions
        self.explosion_timer += dt
        if self.explosion_timer > 0.5:
            self.explosion_timer = 0
            self._create_explosion(
                random.randint(100, SCREEN_WIDTH - 100),
                random.randint(100, SCREEN_HEIGHT - 100)
            )
            
        # Lightning effects
        if random.random() < 0.05:
            self.lightning_effects.append({
                'x1': random.randint(0, SCREEN_WIDTH),
                'y1': 0,
                'x2': random.randint(0, SCREEN_WIDTH),
                'y2': SCREEN_HEIGHT,
                'life': 0.2,
                'branches': []
            })
            
        # Screen shake
        self.elevator_shake = 5 + math.sin(self.timer * 10) * 3
        
        # Auto-advance after 5 seconds
        if self.phase_timer > 5.0:
            self.phase = 3
            self.phase_timer = 0
            
    def _update_ready_phase(self, dt):
        """Update ready to play phase."""
        # Pulsing "Press SPACE to begin" text
        self.text_fade = 128 + math.sin(self.timer * 3) * 127
        
        # Calm down effects
        self.elevator_shake *= 0.95
        
    def _update_effects(self, dt):
        """Update visual effects."""
        # Update particles
        for particle in self.particles[:]:
            particle['life'] -= dt
            if particle['life'] <= 0:
                self.particles.remove(particle)
            else:
                particle['x'] += particle['vx'] * dt
                particle['y'] += particle['vy'] * dt
                particle['vy'] += 100 * dt  # Gravity
                
        # Update lightning
        for lightning in self.lightning_effects[:]:
            lightning['life'] -= dt
            if lightning['life'] <= 0:
                self.lightning_effects.remove(lightning)
                
        # Update screen flash
        if self.screen_flash > 0:
            self.screen_flash -= dt * 2
            
    def _create_explosion(self, x, y):
        """Create an explosion effect at given position."""
        colors = [RED, ORANGE, YELLOW, WHITE]
        for _ in range(20):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(50, 200)
            self.particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.uniform(0.5, 1.5),
                'color': random.choice(colors),
                'size': random.randint(3, 8)
            })
            
    def draw(self, screen):
        """Draw the intro scene.
        
        Args:
            screen: Pygame surface
        """
        # Background
        screen.fill(BLACK)
        
        # Draw based on phase
        if self.phase == 0:
            self._draw_title_phase(screen)
        elif self.phase == 1:
            self._draw_story_phase(screen)
        elif self.phase == 2:
            self._draw_action_phase(screen)
        elif self.phase == 3:
            self._draw_ready_phase(screen)
            
        # Draw effects on top
        self._draw_effects(screen)
        
        # Screen flash
        if self.screen_flash > 0:
            flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash_surface.set_alpha(int(255 * self.screen_flash))
            flash_surface.fill(WHITE)
            screen.blit(flash_surface, (0, 0))
            
        # Skip hint
        if self.phase < 3:
            font = pygame.font.Font(None, 20)
            skip_text = font.render("Press SPACE to skip", True, (100, 100, 100))
            screen.blit(skip_text, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 30))
            
    def _draw_title_phase(self, screen):
        """Draw title screen."""
        # Main title
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("TOWER MADNESS", True, WHITE)
        title_text.set_alpha(int(self.text_fade))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_font = pygame.font.Font(None, 36)
        subtitle_text = subtitle_font.render("Elevator Operator", True, CYAN)
        subtitle_text.set_alpha(int(self.text_fade * 0.8))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 80))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Tower silhouette
        if self.text_fade > 128:
            tower_alpha = int((self.text_fade - 128) * 2)
            # Draw building
            for floor in range(-1, 18):
                y = SCREEN_HEIGHT - 100 - floor * 20
                if y > 100 and y < SCREEN_HEIGHT - 50:
                    floor_rect = pygame.Rect(SCREEN_WIDTH // 2 - 60, y, 120, 18)
                    color = (50, 50, 50) if floor % 2 == 0 else (70, 70, 70)
                    pygame.draw.rect(screen, color, floor_rect)
                    
                    # Windows
                    for window in range(3):
                        window_rect = pygame.Rect(
                            SCREEN_WIDTH // 2 - 50 + window * 35,
                            y + 4, 10, 10
                        )
                        window_color = YELLOW if random.random() < 0.3 else (30, 30, 30)
                        pygame.draw.rect(screen, window_color, window_rect)
                        
    def _draw_story_phase(self, screen):
        """Draw story text."""
        font = pygame.font.Font(None, 36)
        
        # Draw visible lines
        y_offset = 100
        for i in range(min(self.current_line + 1, len(self.story_lines))):
            line = self.story_lines[i]
            if line:
                # Determine color based on content
                if "FRONTIER TOWER" in line:
                    color = GOLD
                elif "Good robots" in line:
                    color = CYAN
                elif "Evil robots" in line:
                    color = RED
                elif "ELEVATOR OPERATOR" in line or "SAVE THE TOWER" in line:
                    color = YELLOW
                else:
                    color = WHITE
                    
                text = font.render(line, True, color)
                
                # Fade in effect for current line
                if i == self.current_line:
                    alpha = min(255, self.line_timer * 200)
                    text.set_alpha(int(alpha))
                    
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                screen.blit(text, text_rect)
                
            y_offset += 50
            
    def _draw_action_phase(self, screen):
        """Draw action sequence."""
        # Apply shake
        shake_x = random.randint(-int(self.elevator_shake), int(self.elevator_shake))
        shake_y = random.randint(-int(self.elevator_shake), int(self.elevator_shake))
        
        # Draw elevator shaft in center
        shaft_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 60 + shake_x,
            100 + shake_y,
            120,
            SCREEN_HEIGHT - 200
        )
        pygame.draw.rect(screen, DARK_GRAY, shaft_rect)
        pygame.draw.rect(screen, GRAY, shaft_rect, 3)
        
        # Draw elevator
        elevator_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 40 + shake_x,
            SCREEN_HEIGHT // 2 - 50 + shake_y + math.sin(self.timer * 5) * 20,
            80, 100
        )
        pygame.draw.rect(screen, ELEVATOR_COLOR, elevator_rect)
        pygame.draw.rect(screen, WHITE, elevator_rect, 2)
        
        # Draw robot silhouettes
        for robot in self.robot_silhouettes:
            # Robot body
            pygame.draw.circle(screen, robot['color'], 
                             (int(robot['x']), int(robot['y'])), 
                             robot['size'])
            # Glowing effect
            for i in range(3):
                glow_surface = pygame.Surface((robot['size'] * 4, robot['size'] * 4), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, 
                                 (*robot['color'], 50 - i * 15),
                                 (robot['size'] * 2, robot['size'] * 2),
                                 robot['size'] + i * 5)
                screen.blit(glow_surface, 
                          (robot['x'] - robot['size'] * 2, 
                           robot['y'] - robot['size'] * 2))
                           
        # Draw lightning
        for lightning in self.lightning_effects:
            pygame.draw.line(screen, WHITE, 
                           (lightning['x1'], lightning['y1']),
                           (lightning['x2'], lightning['y2']), 3)
            pygame.draw.line(screen, CYAN, 
                           (lightning['x1'], lightning['y1']),
                           (lightning['x2'], lightning['y2']), 1)
                           
        # Action text
        action_font = pygame.font.Font(None, 48)
        action_text = action_font.render("ROBOTS AT WAR!", True, RED)
        action_rect = action_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(action_text, action_rect)
        
    def _draw_ready_phase(self, screen):
        """Draw ready to play screen."""
        # Title
        title_font = pygame.font.Font(None, 64)
        title_text = title_font.render("READY?", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(title_text, title_rect)
        
        # Start prompt
        prompt_font = pygame.font.Font(None, 36)
        prompt_text = prompt_font.render("Press SPACE to begin your shift", True, YELLOW)
        prompt_text.set_alpha(int(self.text_fade))
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(prompt_text, prompt_rect)
        
        # Controls reminder
        controls_font = pygame.font.Font(None, 24)
        controls = [
            "W/S - Move Elevator",
            "E - Open/Close Doors",
            "Save the tower from chaos!"
        ]
        
        y_offset = SCREEN_HEIGHT // 2 + 120
        for control in controls:
            control_text = controls_font.render(control, True, (150, 150, 150))
            control_rect = control_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(control_text, control_rect)
            y_offset += 30
            
    def _draw_effects(self, screen):
        """Draw visual effects."""
        # Draw particles
        for particle in self.particles:
            alpha = min(255, int(255 * (particle['life'] / 3.0)))
            size = int(particle['size'] * (particle['life'] / 3.0))
            
            # Glow effect
            for i in range(3):
                glow_size = size + i * 2
                glow_alpha = alpha // (i + 1)
                glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, 
                                 (*particle['color'], glow_alpha),
                                 (glow_size, glow_size), glow_size)
                screen.blit(glow_surface, 
                          (particle['x'] - glow_size, particle['y'] - glow_size))
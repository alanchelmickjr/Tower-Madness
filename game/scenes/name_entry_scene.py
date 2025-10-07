"""
Name entry scene for Tower Madness
Arcade-style 3-character name input for high scores
"""

import pygame
from game.core.constants import *

class NameEntryScene:
    """Arcade-style name entry scene for high score submission."""
    
    def __init__(self, score: int, passengers: int, rank: int):
        """Initialize the name entry scene.
        
        Args:
            score: The score achieved
            passengers: Number of passengers delivered
            rank: Rank on the leaderboard (1-10)
        """
        self.score = score
        self.passengers = passengers
        self.rank = rank
        
        # Name entry state
        self.name = ['A', 'A', 'A']  # 3 characters
        self.current_position = 0  # Which character we're editing (0-2)
        self.complete = False
        self.submitted_name = ""
        
        # Available characters (A-Z, 0-9, space)
        self.characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 '
        self.char_indices = [0, 0, 0]  # Index in characters list for each position
        
        # Animation
        self.blink_timer = 0
        self.blink_visible = True
        self.celebration_timer = 0
        self.particle_effects = []
        
        # Fonts
        self.font_huge = pygame.font.Font(None, 96)
        self.font_large = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
    def update(self, dt: float, events: list):
        """Update the name entry scene.
        
        Args:
            dt: Delta time in seconds
            events: List of pygame events
        """
        self.blink_timer += dt
        if self.blink_timer > 0.5:
            self.blink_timer = 0
            self.blink_visible = not self.blink_visible
            
        self.celebration_timer += dt
        
        # Update particle effects
        for particle in self.particle_effects[:]:
            particle['life'] -= dt
            if particle['life'] <= 0:
                self.particle_effects.remove(particle)
            else:
                particle['y'] -= particle['vy'] * dt
                particle['x'] += particle['vx'] * dt
                
        # Handle input
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self._change_character(1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self._change_character(-1)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self._move_position(-1)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self._move_position(1)
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self._submit_name()
                elif event.key == pygame.K_BACKSPACE:
                    self._move_position(-1)
                    
    def _change_character(self, direction: int):
        """Change the current character up or down.
        
        Args:
            direction: 1 for up, -1 for down
        """
        self.char_indices[self.current_position] += direction
        # Wrap around
        if self.char_indices[self.current_position] >= len(self.characters):
            self.char_indices[self.current_position] = 0
        elif self.char_indices[self.current_position] < 0:
            self.char_indices[self.current_position] = len(self.characters) - 1
            
        self.name[self.current_position] = self.characters[self.char_indices[self.current_position]]
        
    def _move_position(self, direction: int):
        """Move to the next/previous character position.
        
        Args:
            direction: 1 for right, -1 for left
        """
        self.current_position += direction
        # Clamp to valid range
        self.current_position = max(0, min(2, self.current_position))
        
    def _submit_name(self):
        """Submit the entered name."""
        self.submitted_name = ''.join(self.name)
        self.complete = True
        
        # Create celebration particles
        for _ in range(50):
            import random
            self.particle_effects.append({
                'x': SCREEN_WIDTH // 2,
                'y': SCREEN_HEIGHT // 2,
                'vx': random.uniform(-200, 200),
                'vy': random.uniform(100, 300),
                'life': random.uniform(1.0, 2.0),
                'color': random.choice([GOLD, YELLOW, ORANGE, CYAN, MAGENTA]),
                'size': random.randint(3, 8)
            })
        
    def draw(self, screen: pygame.Surface):
        """Draw the name entry scene.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Background
        screen.fill(BLACK)
        
        # Draw animated background
        self._draw_background(screen)
        
        # Title
        if self.rank == 1:
            title_text = "🏆 NEW HIGH SCORE! 🏆"
            title_color = GOLD
        elif self.rank <= 3:
            title_text = f"🌟 TOP {self.rank} SCORE! 🌟"
            title_color = YELLOW
        else:
            title_text = f"HIGH SCORE #{self.rank}!"
            title_color = CYAN
            
        title = self.font_large.render(title_text, True, title_color)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)
        
        # Score display
        score_text = self.font_medium.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 170))
        screen.blit(score_text, score_rect)
        
        passengers_text = self.font_small.render(f"Passengers Delivered: {self.passengers}", True, LIGHT_GRAY)
        passengers_rect = passengers_text.get_rect(center=(SCREEN_WIDTH // 2, 210))
        screen.blit(passengers_text, passengers_rect)
        
        # Name entry prompt
        prompt = self.font_medium.render("ENTER YOUR NAME:", True, WHITE)
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, 280))
        screen.blit(prompt, prompt_rect)
        
        # Draw name entry boxes
        self._draw_name_entry(screen)
        
        # Instructions
        instructions = [
            "↑/↓ or W/S: Change Letter",
            "←/→ or A/D: Move Position",
            "SPACE or ENTER: Submit"
        ]
        
        y_offset = SCREEN_HEIGHT - 150
        for instruction in instructions:
            text = self.font_small.render(instruction, True, LIGHT_GRAY)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 30
            
        # Draw particles
        for particle in self.particle_effects:
            alpha = int(255 * (particle['life'] / 2.0))
            color = (*particle['color'][:3], alpha)
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])
                             
    def _draw_background(self, screen: pygame.Surface):
        """Draw animated background."""
        import math
        # Pulsing gradient
        for y in range(0, SCREEN_HEIGHT, 10):
            progress = y / SCREEN_HEIGHT
            pulse = abs(math.sin(self.celebration_timer * 2 + progress * 3))
            
            if self.rank == 1:
                r = int(50 + pulse * 100)
                g = int(30 + pulse * 80)
                b = int(0)
            else:
                r = int(20 + pulse * 30)
                g = int(20 + pulse * 40)
                b = int(40 + pulse * 60)
                
            pygame.draw.rect(screen, (r, g, b), (0, y, SCREEN_WIDTH, 10))
            
    def _draw_name_entry(self, screen: pygame.Surface):
        """Draw the name entry interface."""
        # Character box dimensions
        box_width = 100
        box_height = 120
        spacing = 20
        total_width = (box_width * 3) + (spacing * 2)
        start_x = (SCREEN_WIDTH - total_width) // 2
        y = 350
        
        for i in range(3):
            x = start_x + (i * (box_width + spacing))
            
            # Box background
            box_rect = pygame.Rect(x, y, box_width, box_height)
            
            # Highlight current position
            if i == self.current_position:
                if self.blink_visible:
                    pygame.draw.rect(screen, YELLOW, box_rect)
                    pygame.draw.rect(screen, GOLD, box_rect, 4)
                else:
                    pygame.draw.rect(screen, DARK_GRAY, box_rect)
                    pygame.draw.rect(screen, YELLOW, box_rect, 4)
            else:
                pygame.draw.rect(screen, DARK_GRAY, box_rect)
                pygame.draw.rect(screen, GRAY, box_rect, 2)
                
            # Character
            char_color = WHITE if i == self.current_position else LIGHT_GRAY
            char_text = self.font_huge.render(self.name[i], True, char_color)
            char_rect = char_text.get_rect(center=(x + box_width // 2, y + box_height // 2))
            screen.blit(char_text, char_rect)
            
            # Position indicator
            if i == self.current_position:
                indicator_y = y + box_height + 15
                pygame.draw.polygon(screen, YELLOW, [
                    (x + box_width // 2, indicator_y),
                    (x + box_width // 2 - 10, indicator_y + 15),
                    (x + box_width // 2 + 10, indicator_y + 15)
                ])
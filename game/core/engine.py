"""
Game engine for Tower Madness / Elevator Operator
Manages game states, scenes, and main game loop
"""

import pygame
from game.core.constants import *
from game.scenes.elevator_scene import ElevatorScene

class GameEngine:
    """Main game engine that manages states and scenes."""
    
    def __init__(self, screen, clock):
        """Initialize the game engine.
        
        Args:
            screen: Pygame display surface
            clock: Pygame clock for timing
        """
        self.screen = screen
        self.clock = clock
        self.running = True
        self.state = STATE_MENU
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_title = pygame.font.Font(None, FONT_SIZE_TITLE)
        
        # Initialize scenes
        self.current_scene = None
        self.elevator_scene = None
        
        # Game variables
        self.player_count = 1
        self.score = 0
        self.high_score = 0
        
        # Start screen animation
        self.title_pulse = 0
        self.shaft_animation = 0
        
    def update(self, dt, events):
        """Update game logic.
        
        Args:
            dt: Delta time in seconds
            events: List of pygame events
        """
        if self.state == STATE_MENU:
            self._update_menu(dt, events)
        elif self.state == STATE_PLAYING:
            if self.elevator_scene:
                self.elevator_scene.update(dt, events)
                # Check for pause
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.state = STATE_PAUSED
        elif self.state == STATE_PAUSED:
            self._update_paused(dt, events)
        elif self.state == STATE_GAME_OVER:
            self._update_game_over(dt, events)
            
    def draw(self):
        """Draw the current game state."""
        self.screen.fill(BLACK)
        
        if self.state == STATE_MENU:
            self._draw_menu()
        elif self.state == STATE_PLAYING:
            if self.elevator_scene:
                self.elevator_scene.draw(self.screen)
        elif self.state == STATE_PAUSED:
            self._draw_paused()
        elif self.state == STATE_GAME_OVER:
            self._draw_game_over()
            
    def _update_menu(self, dt, events):
        """Update menu state."""
        self.title_pulse += dt * 2
        self.shaft_animation += dt * 50
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == ARCADE_BUTTON_1:
                    self._start_game(1)
                    print("Starting single player game!")  # Debug
                elif event.key == pygame.K_2:
                    self._start_game(2)
                    print("Starting two player game!")  # Debug
                    
    def _draw_menu(self):
        """Draw the main menu with elevator shaft visualization."""
        # Draw elevator shaft background
        self._draw_elevator_shaft_background()
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw title with pulsing effect
        pulse = abs(pygame.math.Vector2(1, 0).rotate(self.title_pulse * 100).x)
        title_color = (
            255,
            int(100 + 155 * pulse),
            int(100 + 155 * pulse)
        )
        
        title_text = self.font_title.render("TOWER MADNESS", True, title_color)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = self.font_large.render("Elevator Operator", True, CYAN)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw narrative hints
        narrative_lines = [
            "Floor 4: Good Robot Lab - Where love conquers evil",
            "Basement: Evil Robot Fight Club - Red-lit chaos below",
            "You are the operator caught between two worlds"
        ]
        
        y_offset = 320
        for line in narrative_lines:
            text = self.font_small.render(line, True, LIGHT_GRAY)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, rect)
            y_offset += 30
            
        # Draw start instructions
        start_text = self.font_large.render("Press SPACE to Start", True, WHITE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
        self.screen.blit(start_text, start_rect)
        
        # Draw 2-player option
        two_player_text = self.font_medium.render("Press 2 for Two Players", True, YELLOW)
        two_player_rect = two_player_text.get_rect(center=(SCREEN_WIDTH // 2, 540))
        self.screen.blit(two_player_text, two_player_rect)
        
        # Draw arcade ready text
        arcade_text = self.font_small.render("SF Tech Week Algorave - Arcade Cabinet Ready", True, MAGENTA)
        arcade_rect = arcade_text.get_rect(center=(SCREEN_WIDTH // 2, 700))
        self.screen.blit(arcade_text, arcade_rect)
        
    def _draw_elevator_shaft_background(self):
        """Draw animated elevator shaft visualization."""
        # Draw shaft
        shaft_rect = pygame.Rect(SHAFT_X, 0, SHAFT_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, DARK_GRAY, shaft_rect)
        pygame.draw.rect(self.screen, GRAY, shaft_rect, 3)
        
        # Draw floors
        for floor_num, floor_data in FLOORS.items():
            y = SCREEN_HEIGHT - (floor_num + 2) * FLOOR_HEIGHT
            
            # Draw floor platform
            floor_rect = pygame.Rect(SHAFT_X - 50, y, SHAFT_WIDTH + 100, 5)
            pygame.draw.rect(self.screen, floor_data["color"], floor_rect)
            
            # Draw floor number
            floor_text = self.font_small.render(str(floor_num), True, WHITE)
            text_rect = floor_text.get_rect(center=(SHAFT_X - 25, y - 10))
            self.screen.blit(floor_text, text_rect)
            
            # Special highlighting for narrative floors
            if floor_num == 4:  # Good Robot Lab
                glow_rect = pygame.Rect(SHAFT_X - 60, y - 30, SHAFT_WIDTH + 120, 40)
                pygame.draw.rect(self.screen, CYAN, glow_rect, 2)
            elif floor_num == -1:  # Evil Robot Fight Club
                glow_rect = pygame.Rect(SHAFT_X - 60, y - 30, SHAFT_WIDTH + 120, 40)
                pygame.draw.rect(self.screen, RED, glow_rect, 2)
                
        # Draw animated elevator cables
        cable_offset = int(self.shaft_animation) % 20
        for i in range(0, SCREEN_HEIGHT, 20):
            pygame.draw.line(
                self.screen,
                CABLE_COLOR,
                (SHAFT_X + SHAFT_WIDTH // 2 - 2, i + cable_offset),
                (SHAFT_X + SHAFT_WIDTH // 2 - 2, i + cable_offset + 10),
                2
            )
            pygame.draw.line(
                self.screen,
                CABLE_COLOR,
                (SHAFT_X + SHAFT_WIDTH // 2 + 2, i + cable_offset),
                (SHAFT_X + SHAFT_WIDTH // 2 + 2, i + cable_offset + 10),
                2
            )
            
    def _start_game(self, player_count):
        """Start the game with specified number of players."""
        self.player_count = player_count
        self.state = STATE_PLAYING
        self.elevator_scene = ElevatorScene(self.player_count)
        self.score = 0
        
    def _update_paused(self, dt, events):
        """Update paused state."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.state = STATE_PLAYING
                    
    def _draw_paused(self):
        """Draw paused screen."""
        # Draw the game scene darkened
        if self.elevator_scene:
            self.elevator_scene.draw(self.screen)
            
        # Draw overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw paused text
        paused_text = self.font_title.render("PAUSED", True, WHITE)
        paused_rect = paused_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(paused_text, paused_rect)
        
        resume_text = self.font_medium.render("Press P or ESC to Resume", True, WHITE)
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(resume_text, resume_rect)
        
    def _update_game_over(self, dt, events):
        """Update game over state."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == ARCADE_BUTTON_1:
                    self.state = STATE_MENU
                    
    def _draw_game_over(self):
        """Draw game over screen."""
        # Draw final score
        game_over_text = self.font_title.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        score_text = self.font_large.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(score_text, score_rect)
        
        if self.score > self.high_score:
            self.high_score = self.score
            high_score_text = self.font_medium.render("NEW HIGH SCORE!", True, YELLOW)
            high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            self.screen.blit(high_score_text, high_score_rect)
            
        restart_text = self.font_medium.render("Press SPACE to Return to Menu", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
        self.screen.blit(restart_text, restart_rect)
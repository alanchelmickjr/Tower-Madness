"""
Game engine for Tower Madness / Elevator Operator
Manages game states, scenes, and main game loop
"""

import pygame
from game.core.constants import *
from game.scenes.elevator_scene import ElevatorScene
from game.scenes.name_entry_scene import NameEntryScene
from game.core.leaderboard import LeaderboardManager
from game.core.sound_manager import get_sound_manager

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
        self.name_entry_scene = None
        
        # Initialize leaderboard and sound systems
        self.leaderboard = LeaderboardManager()
        self.sound_manager = get_sound_manager()
        
        # Game variables
        self.player_count = 1
        self.score = 0
        self.passengers_delivered = 0
        self.high_score = self.leaderboard.get_high_score()
        
        # Start screen animation
        self.title_pulse = 0
        self.shaft_animation = 0
        
        # New high score celebration
        self.new_high_score_achieved = False
        self.high_score_rank = 0
        
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
                result = self.elevator_scene.update(dt, events)
                # Update score from scene
                self.score = self.elevator_scene.score
                self.passengers_delivered = self.elevator_scene.passengers_delivered
                
                # Check if scene returned game over state
                if result == STATE_GAME_OVER:
                    self.state = STATE_GAME_OVER
                    self.sound_manager.play_sfx('game_over')
                    print(f"Game Over! Final Score: {self.score}, Passengers: {self.passengers_delivered}")
                
                # Check for pause
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.state = STATE_PAUSED
                            self.sound_manager.play_sfx('pause')
        elif self.state == STATE_PAUSED:
            self._update_paused(dt, events)
        elif self.state == STATE_GAME_OVER:
            self._update_game_over(dt, events)
        elif self.state == STATE_NAME_ENTRY:
            self._update_name_entry(dt, events)
            
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
        elif self.state == STATE_NAME_ENTRY:
            self._draw_name_entry()
            
    def _update_menu(self, dt, events):
        """Update menu state."""
        self.title_pulse += dt * 2
        self.shaft_animation += dt * 50
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == ARCADE_BUTTON_1:
                    self.sound_manager.play_sfx('menu_select')
                    self._start_game(1)
                    print("Starting single player game!")  # Debug
                elif event.key == pygame.K_2:
                    self.sound_manager.play_sfx('menu_select')
                    self._start_game(2)
                    print("Starting two player game!")  # Debug
                    
    def _draw_menu(self):
        """Draw the main menu with leaderboard display."""
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
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = self.font_large.render("Elevator Operator", True, CYAN)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw leaderboards side by side
        self._draw_leaderboards()
        
        # Draw start instructions
        start_text = self.font_large.render("Press SPACE to Start", True, WHITE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, 650))
        self.screen.blit(start_text, start_rect)
        
        # Draw 2-player option
        two_player_text = self.font_medium.render("Press 2 for Two Players", True, YELLOW)
        two_player_rect = two_player_text.get_rect(center=(SCREEN_WIDTH // 2, 690))
        self.screen.blit(two_player_text, two_player_rect)
        
        # Draw arcade ready text
        arcade_text = self.font_small.render("SF Tech Week Algorave - Arcade Cabinet Ready", True, MAGENTA)
        arcade_rect = arcade_text.get_rect(center=(SCREEN_WIDTH // 2, 730))
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
        self.passengers_delivered = 0
        self.new_high_score_achieved = False
        self.sound_manager.play_sfx('game_start')
        
    def _update_paused(self, dt, events):
        """Update paused state."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.state = STATE_PLAYING
                    self.sound_manager.play_sfx('pause')
                    
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
                    # Check if this is a high score
                    if self.leaderboard.is_high_score(self.score):
                        # Go to name entry
                        rank = self._calculate_rank(self.score)
                        self.name_entry_scene = NameEntryScene(self.score, self.passengers_delivered, rank)
                        self.state = STATE_NAME_ENTRY
                        self.sound_manager.play_sfx('high_score')
                    else:
                        # Return to menu
                        self.state = STATE_MENU
                        self.sound_manager.play_sfx('menu_select')
                        
    def _draw_game_over(self):
        """Draw game over screen."""
        # Draw final score
        game_over_text = self.font_title.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        score_text = self.font_large.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(score_text, score_rect)
        
        passengers_text = self.font_medium.render(f"Passengers Delivered: {self.passengers_delivered}", True, LIGHT_GRAY)
        passengers_rect = passengers_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(passengers_text, passengers_rect)
        
        # Check if high score
        if self.leaderboard.is_high_score(self.score):
            rank = self._calculate_rank(self.score)
            if rank == 1:
                high_score_text = self.font_large.render("🏆 NEW HIGH SCORE! 🏆", True, GOLD)
            elif rank <= 3:
                high_score_text = self.font_large.render(f"🌟 TOP {rank} SCORE! 🌟", True, YELLOW)
            else:
                high_score_text = self.font_medium.render(f"High Score #{rank}!", True, CYAN)
            high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            self.screen.blit(high_score_text, high_score_rect)
            
            prompt_text = self.font_medium.render("Press SPACE to Enter Your Name", True, WHITE)
        else:
            prompt_text = self.font_medium.render("Press SPACE to Return to Menu", True, WHITE)
            
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
        self.screen.blit(prompt_text, prompt_rect)
        
    def _update_name_entry(self, dt, events):
        """Update name entry state."""
        if self.name_entry_scene:
            self.name_entry_scene.update(dt, events)
            
            if self.name_entry_scene.complete:
                # Submit score to leaderboard
                result = self.leaderboard.add_score(
                    self.name_entry_scene.submitted_name,
                    self.score,
                    self.passengers_delivered
                )
                
                # Update high score
                self.high_score = self.leaderboard.get_high_score()
                
                # Return to menu
                self.state = STATE_MENU
                self.name_entry_scene = None
                
    def _draw_name_entry(self):
        """Draw name entry screen."""
        if self.name_entry_scene:
            self.name_entry_scene.draw(self.screen)
            
    def _draw_leaderboards(self):
        """Draw all-time and session leaderboards side by side."""
        # Left panel: All-Time Top 10
        left_x = 50
        left_y = 220
        panel_width = 450
        panel_height = 400
        
        # Draw all-time panel
        all_time_bg = pygame.Rect(left_x, left_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, (0, 0, 0, 200), all_time_bg)
        pygame.draw.rect(self.screen, GOLD, all_time_bg, 3)
        
        # All-time title
        all_time_title = self.font_large.render("🏆 ALL-TIME TOP 10", True, GOLD)
        title_rect = all_time_title.get_rect(center=(left_x + panel_width // 2, left_y + 30))
        self.screen.blit(all_time_title, title_rect)
        
        # All-time scores
        all_time_scores = self.leaderboard.get_top_scores(10)
        y_offset = left_y + 70
        
        if all_time_scores:
            for i, entry in enumerate(all_time_scores):
                rank = i + 1
                name = entry['name']
                score = entry['score']
                
                # Rank color
                if rank == 1:
                    rank_color = GOLD
                elif rank == 2:
                    rank_color = (192, 192, 192)  # Silver
                elif rank == 3:
                    rank_color = (205, 127, 50)  # Bronze
                else:
                    rank_color = WHITE
                    
                # Draw entry
                rank_text = self.font_medium.render(f"{rank}.", True, rank_color)
                name_text = self.font_medium.render(name, True, rank_color)
                score_text = self.font_medium.render(str(score), True, rank_color)
                
                self.screen.blit(rank_text, (left_x + 20, y_offset))
                self.screen.blit(name_text, (left_x + 70, y_offset))
                self.screen.blit(score_text, (left_x + panel_width - 120, y_offset))
                
                y_offset += 32
        else:
            no_scores_text = self.font_small.render("No scores yet - be the first!", True, LIGHT_GRAY)
            no_scores_rect = no_scores_text.get_rect(center=(left_x + panel_width // 2, left_y + 200))
            self.screen.blit(no_scores_text, no_scores_rect)
        
        # Right panel: Session Top 5
        right_x = SCREEN_WIDTH - panel_width - 50
        right_y = 220
        
        # Draw session panel
        session_bg = pygame.Rect(right_x, right_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, (0, 0, 0, 200), session_bg)
        pygame.draw.rect(self.screen, CYAN, session_bg, 3)
        
        # Session title
        session_title = self.font_large.render("📊 SESSION TOP 5", True, CYAN)
        title_rect = session_title.get_rect(center=(right_x + panel_width // 2, right_y + 30))
        self.screen.blit(session_title, title_rect)
        
        # Session scores
        session_scores = self.leaderboard.get_session_scores(5)
        y_offset = right_y + 70
        
        if session_scores:
            for i, entry in enumerate(session_scores):
                rank = i + 1
                name = entry['name']
                score = entry['score']
                
                # Draw entry
                rank_text = self.font_medium.render(f"{rank}.", True, CYAN)
                name_text = self.font_medium.render(name, True, WHITE)
                score_text = self.font_medium.render(str(score), True, WHITE)
                
                self.screen.blit(rank_text, (right_x + 20, y_offset))
                self.screen.blit(name_text, (right_x + 70, y_offset))
                self.screen.blit(score_text, (right_x + panel_width - 120, y_offset))
                
                y_offset += 32
        else:
            no_scores_text = self.font_small.render("No scores this session yet", True, LIGHT_GRAY)
            no_scores_rect = no_scores_text.get_rect(center=(right_x + panel_width // 2, right_y + 200))
            self.screen.blit(no_scores_text, no_scores_rect)
            
    def _calculate_rank(self, score):
        """Calculate what rank a score would achieve.
        
        Args:
            score: The score to check
            
        Returns:
            Rank (1-based) the score would achieve
        """
        all_time_scores = self.leaderboard.get_top_scores(10)
        rank = 1
        for entry in all_time_scores:
            if score > entry['score']:
                break
            rank += 1
        return rank
"""
Special NPCs for Tower Madness / Elevator Operator
Each floor has unique characters with personalities
"""

import pygame
import random
from game.core.constants import *
from game.entities.npc import NPC

class SpecialNPC(NPC):
    """Base class for special named NPCs."""
    
    def __init__(self, x, y, name, floor_num, color=None):
        super().__init__(x, y, "special")
        self.name = name
        self.home_floor = floor_num
        self.current_floor = floor_num
        self.special_color = color or (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.dialogue = []
        self.font = pygame.font.Font(None, 16)
        
    def draw(self, screen):
        """Draw the special NPC with their name."""
        # Draw the NPC body
        self._draw_special_character(screen)
        
        # Draw name above NPC
        name_text = self.font.render(self.name, True, WHITE)
        name_rect = name_text.get_rect(center=(self.rect.centerx, self.rect.top - 10))
        
        # Draw background for name
        bg_rect = name_rect.inflate(4, 2)
        pygame.draw.rect(screen, BLACK, bg_rect)
        pygame.draw.rect(screen, self.special_color, bg_rect, 1)
        
        screen.blit(name_text, name_rect)
        
        # Draw destination indicator
        dest_text = self.font.render(f"→F{self.destination_floor}", True, YELLOW)
        dest_rect = dest_text.get_rect(center=(self.rect.centerx, self.rect.bottom + 10))
        screen.blit(dest_text, dest_rect)
        
    def _draw_special_character(self, screen):
        """Draw the character sprite."""
        # Draw retro pixel-art style character
        pygame.draw.rect(screen, self.special_color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Draw simple face
        eye_y = self.rect.top + 10
        pygame.draw.circle(screen, WHITE, (self.rect.left + 8, eye_y), 3)
        pygame.draw.circle(screen, WHITE, (self.rect.right - 8, eye_y), 3)
        pygame.draw.circle(screen, BLACK, (self.rect.left + 8, eye_y), 1)
        pygame.draw.circle(screen, BLACK, (self.rect.right - 8, eye_y), 1)


class JohnTheDoorman(SpecialNPC):
    """John - The friendly android doorman at street level."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "John", 0, color=(50, 50, 150))
        self.destination_floor = random.choice([1, 2, 3])
        self.patience = 999
        self.dialogue = [
            "Welcome to Frontier Tower!",
            "Have a great day!",
            "I'll keep the entrance secure."
        ]
        
    def _draw_special_character(self, screen):
        """Draw John in doorman uniform."""
        # Blue uniform
        pygame.draw.rect(screen, (50, 50, 150), self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Draw doorman cap
        cap_rect = pygame.Rect(self.rect.x + 2, self.rect.y - 5, self.rect.width - 4, 8)
        pygame.draw.rect(screen, (30, 30, 100), cap_rect)
        pygame.draw.rect(screen, BLACK, cap_rect, 1)
        
        # Draw badge
        badge_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 15, 6, 6)
        pygame.draw.rect(screen, GOLD, badge_rect)
        
        # Draw friendly face
        eye_y = self.rect.top + 10
        pygame.draw.circle(screen, WHITE, (self.rect.left + 8, eye_y), 3)
        pygame.draw.circle(screen, WHITE, (self.rect.right - 8, eye_y), 3)
        pygame.draw.circle(screen, BLACK, (self.rect.left + 8, eye_y), 1)
        pygame.draw.circle(screen, BLACK, (self.rect.right - 8, eye_y), 1)
        
        # Smile
        pygame.draw.arc(screen, BLACK, 
                       pygame.Rect(self.rect.centerx - 5, self.rect.centery - 5, 10, 10),
                       0, 3.14, 2)


class XenoThePhilosopher(SpecialNPC):
    """Xeno - Philosopher and thinker."""
    
    def __init__(self, x, y, floor_num):
        super().__init__(x, y, "Xeno", floor_num, color=(200, 100, 200))
        self.destination_floor = random.choice([14, 15, 17])  # Likes intellectual floors
        self.patience = 120
        self.dialogue = [
            "What is the nature of existence?",
            "The elevator is a metaphor for life.",
            "Up or down, it's all relative."
        ]
        
    def _draw_special_character(self, screen):
        """Draw Xeno with philosopher robes."""
        # Purple robes
        pygame.draw.rect(screen, (200, 100, 200), self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Draw beard
        beard_rect = pygame.Rect(self.rect.x + 8, self.rect.y + 20, self.rect.width - 16, 10)
        pygame.draw.rect(screen, GRAY, beard_rect)
        
        # Thoughtful eyes
        eye_y = self.rect.top + 10
        pygame.draw.circle(screen, WHITE, (self.rect.left + 8, eye_y), 3)
        pygame.draw.circle(screen, WHITE, (self.rect.right - 8, eye_y), 3)
        pygame.draw.circle(screen, BLACK, (self.rect.left + 9, eye_y - 1), 1)
        pygame.draw.circle(screen, BLACK, (self.rect.right - 9, eye_y - 1), 1)


class VitaliaTheHealer(SpecialNPC):
    """Vitalia - Health and wellness expert."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Vitalia", 3, color=(100, 200, 100))
        self.destination_floor = random.choice([11, 8, 5])  # Health-related floors
        self.patience = 90
        self.dialogue = [
            "Health is wealth!",
            "Take care of yourself.",
            "Mind, body, and soul."
        ]
        
    def _draw_special_character(self, screen):
        """Draw Vitalia in medical/wellness attire."""
        # Green health theme
        pygame.draw.rect(screen, (100, 200, 100), self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Draw medical cross
        cross_x = self.rect.centerx
        cross_y = self.rect.centery
        pygame.draw.rect(screen, WHITE, (cross_x - 1, cross_y - 4, 2, 8))
        pygame.draw.rect(screen, WHITE, (cross_x - 4, cross_y - 1, 8, 2))
        
        # Caring eyes
        eye_y = self.rect.top + 10
        pygame.draw.circle(screen, WHITE, (self.rect.left + 8, eye_y), 3)
        pygame.draw.circle(screen, WHITE, (self.rect.right - 8, eye_y), 3)
        pygame.draw.circle(screen, (50, 150, 50), (self.rect.left + 8, eye_y), 1)
        pygame.draw.circle(screen, (50, 150, 50), (self.rect.right - 8, eye_y), 1)


class VitalyTheBuilder(SpecialNPC):
    """Vitaly - Construction and building expert."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Vitaly", 4, color=(150, 100, 50))
        self.destination_floor = random.choice([5, 7, 2])  # Construction/maker floors
        self.patience = 80
        self.dialogue = [
            "Building the future!",
            "Measure twice, cut once.",
            "Hard work pays off."
        ]
        
    def _draw_special_character(self, screen):
        """Draw Vitaly in construction gear."""
        # Brown work clothes
        pygame.draw.rect(screen, (150, 100, 50), self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Draw hard hat
        hat_rect = pygame.Rect(self.rect.x + 3, self.rect.y - 3, self.rect.width - 6, 6)
        pygame.draw.rect(screen, YELLOW, hat_rect)
        pygame.draw.rect(screen, BLACK, hat_rect, 1)
        
        # Draw tool belt
        belt_rect = pygame.Rect(self.rect.x, self.rect.centery + 5, self.rect.width, 4)
        pygame.draw.rect(screen, (100, 50, 0), belt_rect)
        
        # Strong eyes
        eye_y = self.rect.top + 10
        pygame.draw.circle(screen, WHITE, (self.rect.left + 8, eye_y), 3)
        pygame.draw.circle(screen, WHITE, (self.rect.right - 8, eye_y), 3)
        pygame.draw.circle(screen, BLACK, (self.rect.left + 8, eye_y), 1)
        pygame.draw.circle(screen, BLACK, (self.rect.right - 8, eye_y), 1)


class XeniaTheArtist(SpecialNPC):
    """Xenia - Creative artist."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Xenia", 4, color=(255, 100, 255))
        self.destination_floor = random.choice([6, 2, 16])  # Creative floors
        self.patience = 100
        self.dialogue = [
            "Art is life!",
            "Express yourself!",
            "Beauty is everywhere."
        ]
        
    def _draw_special_character(self, screen):
        """Draw Xenia in artistic attire."""
        # Colorful artistic theme
        colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]
        color_index = int(self.animation_frame) % len(colors)
        pygame.draw.rect(screen, colors[color_index], self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Draw beret
        beret_rect = pygame.Rect(self.rect.x + 5, self.rect.y - 2, self.rect.width - 8, 5)
        pygame.draw.ellipse(screen, (50, 50, 50), beret_rect)
        
        # Artistic eyes
        eye_y = self.rect.top + 10
        pygame.draw.circle(screen, WHITE, (self.rect.left + 8, eye_y), 3)
        pygame.draw.circle(screen, WHITE, (self.rect.right - 8, eye_y), 3)
        pygame.draw.circle(screen, MAGENTA, (self.rect.left + 8, eye_y), 1)
        pygame.draw.circle(screen, CYAN, (self.rect.right - 8, eye_y), 1)


class ScottTheMusician(SpecialNPC):
    """Scott - Musician on the Arts & Music floor."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Scott", 6, color=(150, 50, 200))
        self.destination_floor = random.choice([2, 16, 17])  # Event/party floors
        self.patience = 75
        self.dialogue = [
            "Music is the universal language!",
            "Feel the rhythm!",
            "Let's jam!"
        ]
        
    def _draw_special_character(self, screen):
        """Draw Scott with musical theme."""
        # Purple musician theme
        pygame.draw.rect(screen, (150, 50, 200), self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Draw headphones
        pygame.draw.arc(screen, BLACK, 
                       pygame.Rect(self.rect.x + 5, self.rect.y - 5, self.rect.width - 10, 15),
                       0, 3.14, 3)
        pygame.draw.circle(screen, BLACK, (self.rect.left + 5, self.rect.top + 5), 3)
        pygame.draw.circle(screen, BLACK, (self.rect.right - 5, self.rect.top + 5), 3)
        
        # Musical note on chest
        note_x = self.rect.centerx
        note_y = self.rect.centery
        pygame.draw.circle(screen, BLACK, (note_x, note_y + 3), 2)
        pygame.draw.line(screen, BLACK, (note_x + 2, note_y + 3), (note_x + 2, note_y - 3), 2)
        
        # Cool eyes with sunglasses
        pygame.draw.rect(screen, BLACK, (self.rect.left + 5, self.rect.top + 8, 20, 6))


class TonyTheMaker(SpecialNPC):
    """Tony - Maker and inventor."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Tony", 7, color=(100, 150, 200))
        self.destination_floor = random.choice([4, 8, 9])  # Tech floors
        self.patience = 85
        self.dialogue = [
            "Let's build something amazing!",
            "Innovation is key!",
            "Prototype and iterate!"
        ]
        
    def _draw_special_character(self, screen):
        """Draw Tony with maker/inventor theme."""
        # Blue tech theme
        pygame.draw.rect(screen, (100, 150, 200), self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Draw goggles
        pygame.draw.circle(screen, GRAY, (self.rect.left + 8, self.rect.top + 10), 4)
        pygame.draw.circle(screen, GRAY, (self.rect.right - 8, self.rect.top + 10), 4)
        pygame.draw.line(screen, BLACK, (self.rect.left + 12, self.rect.top + 10),
                        (self.rect.right - 12, self.rect.top + 10), 1)
        
        # Draw wrench in hand
        pygame.draw.rect(screen, GRAY, (self.rect.right - 5, self.rect.centery, 8, 3))
        
        # Focused eyes
        pygame.draw.circle(screen, WHITE, (self.rect.left + 8, self.rect.top + 10), 2)
        pygame.draw.circle(screen, WHITE, (self.rect.right - 8, self.rect.top + 10), 2)
        pygame.draw.circle(screen, BLACK, (self.rect.left + 8, self.rect.top + 10), 1)
        pygame.draw.circle(screen, BLACK, (self.rect.right - 8, self.rect.top + 10), 1)


class CindyTheEngineer(SpecialNPC):
    """Cindy - Engineer and problem solver."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Cindy", 7, color=(200, 150, 100))
        self.destination_floor = random.choice([4, 9, 10])  # Tech/business floors
        self.patience = 90
        self.dialogue = [
            "Engineering solutions!",
            "Problem solved!",
            "Optimize everything!"
        ]
        
    def _draw_special_character(self, screen):
        """Draw Cindy with engineering theme."""
        # Orange engineer theme
        pygame.draw.rect(screen, (200, 150, 100), self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Draw safety vest
        vest_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 12, self.rect.width - 4, 15)
        pygame.draw.rect(screen, YELLOW, vest_rect)
        pygame.draw.rect(screen, BLACK, vest_rect, 1)
        
        # Draw clipboard
        pygame.draw.rect(screen, WHITE, (self.rect.left + 2, self.rect.centery, 8, 10))
        pygame.draw.rect(screen, BLACK, (self.rect.left + 2, self.rect.centery, 8, 10), 1)
        
        # Smart eyes
        eye_y = self.rect.top + 10
        pygame.draw.circle(screen, WHITE, (self.rect.left + 8, eye_y), 3)
        pygame.draw.circle(screen, WHITE, (self.rect.right - 8, eye_y), 3)
        pygame.draw.circle(screen, BLACK, (self.rect.left + 8, eye_y), 1)
        pygame.draw.circle(screen, BLACK, (self.rect.right - 8, eye_y), 1)


class LaurenceTheInvestor(SpecialNPC):
    """Laurence - Health and longevity investor."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "Laurence", 11, color=(50, 100, 50))
        self.destination_floor = random.choice([10, 8, 12])  # Business/tech floors
        self.patience = 100
        self.dialogue = [
            "Investing in the future of health!",
            "Longevity is the next frontier.",
            "ROI on wellness is infinite."
        ]
        
    def _draw_special_character(self, screen):
        """Draw Laurence in business attire."""
        # Dark green business suit
        pygame.draw.rect(screen, (50, 100, 50), self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Draw tie
        tie_rect = pygame.Rect(self.rect.centerx - 2, self.rect.y + 12, 4, 15)
        pygame.draw.rect(screen, RED, tie_rect)
        
        # Draw briefcase
        case_rect = pygame.Rect(self.rect.right - 10, self.rect.centery + 5, 10, 8)
        pygame.draw.rect(screen, (50, 50, 50), case_rect)
        pygame.draw.rect(screen, BLACK, case_rect, 1)
        
        # Business eyes
        eye_y = self.rect.top + 10
        pygame.draw.circle(screen, WHITE, (self.rect.left + 8, eye_y), 3)
        pygame.draw.circle(screen, WHITE, (self.rect.right - 8, eye_y), 3)
        pygame.draw.circle(screen, BLACK, (self.rect.left + 8, eye_y), 1)
        pygame.draw.circle(screen, BLACK, (self.rect.right - 8, eye_y), 1)
        
        # Glasses
        pygame.draw.circle(screen, BLACK, (self.rect.left + 8, eye_y), 4, 1)
        pygame.draw.circle(screen, BLACK, (self.rect.right - 8, eye_y), 4, 1)
        pygame.draw.line(screen, BLACK, (self.rect.left + 12, eye_y), (self.rect.right - 12, eye_y), 1)


# Factory function to create special NPCs
def create_special_npc(floor_num, x, y):
    """Create the appropriate special NPC for a given floor."""
    special_npcs = {
        0: lambda: JohnTheDoorman(x, y),
        2: lambda: XenoThePhilosopher(x, y, 2),
        3: lambda: VitaliaTheHealer(x, y),
        4: lambda: random.choice([VitalyTheBuilder(x, y), XeniaTheArtist(x, y)]),
        6: lambda: ScottTheMusician(x, y),
        7: lambda: random.choice([TonyTheMaker(x, y), CindyTheEngineer(x, y)]),
        11: lambda: LaurenceTheInvestor(x, y),
        16: lambda: XenoThePhilosopher(x, y, 16),
    }
    
    if floor_num in special_npcs:
        return special_npcs[floor_num]()
    return None

"""
AI-powered sprite generator for Tower Madness NPCs
Uses OpenAI to generate unique pixel art descriptions and converts them to sprites
"""

import os
import json
import pygame
import random
import hashlib
from typing import Dict, List, Tuple
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

class AISpritGenerator:
    """Generates unique pixel art sprites for NPCs using AI."""
    
    def __init__(self):
        """Initialize the AI sprite generator."""
        self.api_key = os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
        self.sprite_cache = {}
        self.character_descriptions = {
            "John": {
                "description": "older distinguished black gentleman doorman, friendly smile, blue uniform with gold badge, doorman cap",
                "colors": {
                    "skin": (139, 90, 43),
                    "uniform": (50, 50, 150),
                    "badge": (255, 215, 0),
                    "cap": (30, 30, 100),
                    "eyes": (50, 30, 20),
                    "hair": (60, 60, 60)
                }
            },
            "Alan": {
                "description": "the most amazing looking man, perfect features, charismatic leader, bright cyan robotics lab coat, confident stance",
                "colors": {
                    "skin": (255, 220, 177),
                    "coat": (0, 200, 255),
                    "hair": (30, 30, 30),
                    "eyes": (0, 150, 200),
                    "pants": (50, 50, 50)
                }
            },
            "Scott": {
                "description": "long-haired middle-aged musician, headphones, purple shirt, relaxed vibe, artistic soul",
                "colors": {
                    "skin": (255, 205, 148),
                    "hair": (101, 67, 33),
                    "shirt": (150, 50, 200),
                    "headphones": (30, 30, 30),
                    "eyes": (100, 50, 30)
                }
            },
            "Tony": {
                "description": "tall maker with big smile, safety goggles on head, blue work shirt, tool belt, enthusiastic",
                "colors": {
                    "skin": (255, 210, 160),
                    "shirt": (100, 150, 200),
                    "goggles": (150, 150, 150),
                    "belt": (100, 50, 0),
                    "hair": (80, 60, 40),
                    "eyes": (60, 40, 20)
                }
            },
            "Xeno": {
                "description": "Xenofon - short Greek manager who saves the day, glasses, spiky black hair, calming smile",
                "colors": {
                    "skin": (235, 195, 160),
                    "shirt": (100, 150, 200),
                    "pants": (50, 50, 100),
                    "hair": (20, 20, 20),
                    "eyes": (80, 60, 40),
                    "glasses": (150, 150, 150)
                }
            },
            "Vitalia": {
                "description": "health expert, green medical scrubs, caring expression, stethoscope, warm smile",
                "colors": {
                    "skin": (245, 200, 170),
                    "scrubs": (100, 200, 100),
                    "stethoscope": (50, 50, 50),
                    "hair": (150, 100, 50),
                    "eyes": (50, 150, 50)
                }
            },
            "Vitaly": {
                "description": "construction worker, yellow hard hat, brown work clothes, strong build, determined look",
                "colors": {
                    "skin": (240, 190, 150),
                    "clothes": (150, 100, 50),
                    "hardhat": (255, 255, 0),
                    "boots": (50, 30, 20),
                    "eyes": (80, 60, 40)
                }
            },
            "Xenia": {
                "description": "creative artist, colorful attire, beret, paint-splattered apron, expressive eyes",
                "colors": {
                    "skin": (255, 210, 180),
                    "clothes": [(255, 100, 100), (100, 255, 100), (100, 100, 255)],
                    "beret": (50, 50, 50),
                    "hair": (200, 150, 100),
                    "eyes": (150, 100, 200)
                }
            },
            "Cindy": {
                "description": "engineer with safety vest, clipboard, orange hard hat, analytical expression",
                "colors": {
                    "skin": (250, 205, 175),
                    "vest": (255, 255, 0),
                    "shirt": (200, 150, 100),
                    "hardhat": (255, 165, 0),
                    "hair": (100, 80, 60),
                    "eyes": (60, 60, 60)
                }
            },
            "Laurence": {
                "description": "distinguished investor, dark green business suit, glasses, briefcase, professional demeanor",
                "colors": {
                    "skin": (240, 200, 170),
                    "suit": (50, 100, 50),
                    "tie": (200, 0, 0),
                    "glasses": (200, 200, 200),
                    "hair": (80, 80, 80),
                    "eyes": (50, 50, 50)
                }
            },
            "Morgan": {
                "description": "tall thin bald biotech researcher on floor 8, lab coat, says 'lets scan your brain'",
                "colors": {
                    "skin": (245, 210, 180),
                    "coat": (255, 255, 255),
                    "shirt": (100, 200, 100),
                    "scalp": (235, 200, 170),  # Bald head
                    "eyes": (60, 120, 60)
                }
            },
            "China": {
                "description": "tiny elegant Chinese accelerator leader on floor 10, sharp business attire, gold accents",
                "colors": {
                    "skin": (255, 230, 200),
                    "suit": (30, 30, 30),
                    "shirt": (255, 215, 0),
                    "hair": (20, 20, 20),
                    "eyes": (40, 30, 20)
                }
            },
            "Devinder": {
                "description": "tall handsome Indian AI researcher on floor 9, futuristic style, blue tech wear",
                "colors": {
                    "skin": (180, 140, 100),
                    "clothes": (100, 100, 200),
                    "accent": (0, 200, 255),
                    "hair": (20, 20, 20),
                    "eyes": (50, 30, 20)
                }
            },
            "Cindy": {
                "description": "thin short Asian engineer (secretly a robot), orange safety gear, glowing eyes",
                "colors": {
                    "skin": (255, 235, 210),  # Asian skin tone with slight metallic hint
                    "vest": (255, 255, 0),
                    "shirt": (200, 150, 100),
                    "hardhat": (255, 165, 0),
                    "hair": (20, 20, 20),
                    "eyes": (0, 255, 255),  # Glowing cyan robot eyes
                    "circuits": (0, 200, 255)
                }
            },
            "HeadphoneJames": {
                "description": "mysterious hero with huge headphones and tie-dye shirt, appears randomly to save the day",
                "colors": {
                    "skin": (240, 200, 170),
                    "headphones": (255, 50, 50),  # Red headphones
                    "tiedye": [(255, 100, 200), (100, 255, 200), (200, 100, 255), (255, 255, 100)],  # Tie-dye colors
                    "pants": (100, 100, 100),
                    "hair": (100, 80, 60),
                    "eyes": (100, 100, 200),
                    "cape": (200, 0, 0)  # Hero cape
                }
            }
        }
    
    def generate_pixel_sprite(self, name: str, width: int = 30, height: int = 40) -> pygame.Surface:
        """Generate a detailed pixel art sprite for a character.
        
        Args:
            name: Character name
            width: Sprite width
            height: Sprite height
            
        Returns:
            pygame.Surface with the generated sprite
        """
        # Check cache first
        cache_key = f"{name}_{width}_{height}"
        if cache_key in self.sprite_cache:
            return self.sprite_cache[cache_key]
        
        # Create sprite surface
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.fill((0, 0, 0, 0))  # Transparent background
        
        if name in self.character_descriptions:
            char_data = self.character_descriptions[name]
            colors = char_data["colors"]
            
            # Generate based on character type
            if name == "John":
                self._draw_john(sprite, colors, width, height)
            elif name == "Alan":
                self._draw_alan(sprite, colors, width, height)
            elif name == "Scott":
                self._draw_scott(sprite, colors, width, height)
            elif name == "Tony":
                self._draw_tony(sprite, colors, width, height)
            elif name == "Xeno":
                self._draw_xeno(sprite, colors, width, height)
            elif name == "Vitalia":
                self._draw_vitalia(sprite, colors, width, height)
            elif name == "Vitaly":
                self._draw_vitaly(sprite, colors, width, height)
            elif name == "Xenia":
                self._draw_xenia(sprite, colors, width, height)
            elif name == "Cindy":
                self._draw_cindy(sprite, colors, width, height)
            elif name == "Laurence":
                self._draw_laurence(sprite, colors, width, height)
            elif name == "Morgan":
                self._draw_morgan(sprite, colors, width, height)
            elif name == "China":
                self._draw_china(sprite, colors, width, height)
            elif name == "Devinder":
                self._draw_devinder(sprite, colors, width, height)
            elif name == "HeadphoneJames":
                self._draw_headphone_james(sprite, colors, width, height)
            else:
                self._draw_generic(sprite, width, height)
        else:
            self._draw_generic(sprite, width, height)
        
        # Cache the sprite
        self.sprite_cache[cache_key] = sprite
        return sprite
    
    def _draw_john(self, sprite: pygame.Surface, colors: Dict, width: int, height: int):
        """Draw John the doorman."""
        # Doorman cap
        pygame.draw.rect(sprite, colors["cap"], (5, 2, width-10, 5))
        pygame.draw.rect(sprite, (0, 0, 0), (5, 2, width-10, 5), 1)
        
        # Head (older black gentleman)
        pygame.draw.rect(sprite, colors["skin"], (7, 7, width-14, 12))
        
        # Gray hair on sides
        pygame.draw.rect(sprite, colors["hair"], (5, 9, 3, 8))
        pygame.draw.rect(sprite, colors["hair"], (width-8, 9, 3, 8))
        
        # Eyes
        pygame.draw.rect(sprite, (255, 255, 255), (9, 10, 3, 2))
        pygame.draw.rect(sprite, (255, 255, 255), (width-12, 10, 3, 2))
        pygame.draw.rect(sprite, colors["eyes"], (10, 10, 1, 2))
        pygame.draw.rect(sprite, colors["eyes"], (width-11, 10, 1, 2))
        
        # Friendly smile
        pygame.draw.rect(sprite, (255, 200, 200), (11, 15, width-22, 2))
        
        # Blue uniform body
        pygame.draw.rect(sprite, colors["uniform"], (6, 19, width-12, 15))
        pygame.draw.rect(sprite, (0, 0, 0), (6, 19, width-12, 15), 1)
        
        # Gold badge
        pygame.draw.rect(sprite, colors["badge"], (8, 21, 4, 4))
        pygame.draw.rect(sprite, (0, 0, 0), (8, 21, 4, 4), 1)
        
        # Arms
        pygame.draw.rect(sprite, colors["uniform"], (3, 22, 3, 10))
        pygame.draw.rect(sprite, colors["uniform"], (width-6, 22, 3, 10))
        
        # Hands
        pygame.draw.rect(sprite, colors["skin"], (3, 32, 3, 3))
        pygame.draw.rect(sprite, colors["skin"], (width-6, 32, 3, 3))
        
        # Legs
        pygame.draw.rect(sprite, colors["uniform"], (8, 34, 5, 6))
        pygame.draw.rect(sprite, colors["uniform"], (width-13, 34, 5, 6))
    
    def _draw_alan(self, sprite: pygame.Surface, colors: Dict, width: int, height: int):
        """Draw Alan - the most amazing looking man."""
        # Perfect hair
        pygame.draw.rect(sprite, colors["hair"], (6, 3, width-12, 8))
        for i in range(3):
            pygame.draw.rect(sprite, (colors["hair"][0]-20, colors["hair"][1]-20, colors["hair"][2]-20), 
                           (7+i*3, 3, 2, 6))
        
        # Head with perfect features
        pygame.draw.rect(sprite, colors["skin"], (7, 8, width-14, 11))
        
        # Striking eyes
        pygame.draw.rect(sprite, (255, 255, 255), (9, 11, 4, 3))
        pygame.draw.rect(sprite, (255, 255, 255), (width-13, 11, 4, 3))
        pygame.draw.rect(sprite, colors["eyes"], (10, 12, 2, 2))
        pygame.draw.rect(sprite, colors["eyes"], (width-12, 12, 2, 2))
        # Eye sparkle
        pygame.draw.rect(sprite, (255, 255, 255), (10, 12, 1, 1))
        pygame.draw.rect(sprite, (255, 255, 255), (width-11, 12, 1, 1))
        
        # Perfect smile
        pygame.draw.rect(sprite, (255, 255, 255), (10, 16, width-20, 2))
        
        # Cyan lab coat
        pygame.draw.rect(sprite, colors["coat"], (5, 19, width-10, 18))
        pygame.draw.rect(sprite, (0, 0, 0), (5, 19, width-10, 18), 1)
        
        # Coat details
        pygame.draw.line(sprite, (255, 255, 255), (width//2, 20), (width//2, 35), 1)
        pygame.draw.rect(sprite, (255, 255, 255), (7, 22, 3, 2))
        pygame.draw.rect(sprite, (255, 255, 255), (width-10, 22, 3, 2))
        
        # Arms
        pygame.draw.rect(sprite, colors["coat"], (2, 21, 3, 12))
        pygame.draw.rect(sprite, colors["coat"], (width-5, 21, 3, 12))
        
        # Hands
        pygame.draw.rect(sprite, colors["skin"], (2, 33, 3, 3))
        pygame.draw.rect(sprite, colors["skin"], (width-5, 33, 3, 3))
        
        # Legs
        pygame.draw.rect(sprite, colors["pants"], (8, 37, 5, 3))
        pygame.draw.rect(sprite, colors["pants"], (width-13, 37, 5, 3))
    
    def _draw_scott(self, sprite: pygame.Surface, colors: Dict, width: int, height: int):
        """Draw Scott the musician with long hair."""
        # Long hair
        pygame.draw.rect(sprite, colors["hair"], (5, 4, width-10, 15))
        # Hair texture
        for i in range(5):
            pygame.draw.line(sprite, (colors["hair"][0]-20, colors["hair"][1]-20, colors["hair"][2]-20),
                           (6+i*4, 4), (6+i*4, 18), 1)
        
        # Headphones
        pygame.draw.arc(sprite, colors["headphones"], 
                       pygame.Rect(6, 2, width-12, 10), 0, 3.14, 3)
        pygame.draw.circle(sprite, colors["headphones"], (7, 8), 3)
        pygame.draw.circle(sprite, colors["headphones"], (width-7, 8), 3)
        
        # Head
        pygame.draw.rect(sprite, colors["skin"], (8, 9, width-16, 10))
        
        # Cool sunglasses
        pygame.draw.rect(sprite, (0, 0, 0), (8, 11, width-16, 4))
        pygame.draw.rect(sprite, (50, 50, 50), (9, 12, 5, 2))
        pygame.draw.rect(sprite, (50, 50, 50), (width-14, 12, 5, 2))
        
        # Purple shirt
        pygame.draw.rect(sprite, colors["shirt"], (6, 19, width-12, 14))
        
        # Musical note on shirt
        pygame.draw.circle(sprite, (255, 255, 255), (width//2, 25), 2)
        pygame.draw.line(sprite, (255, 255, 255), (width//2+2, 25), (width//2+2, 22), 2)
        
        # Arms
        pygame.draw.rect(sprite, colors["skin"], (3, 21, 3, 10))
        pygame.draw.rect(sprite, colors["skin"], (width-6, 21, 3, 10))
        
        # Legs
        pygame.draw.rect(sprite, (50, 50, 100), (8, 33, 5, 7))
        pygame.draw.rect(sprite, (50, 50, 100), (width-13, 33, 5, 7))
    
    def _draw_tony(self, sprite: pygame.Surface, colors: Dict, width: int, height: int):
        """Draw Tony the tall maker with big smile."""
        # Hair
        pygame.draw.rect(sprite, colors["hair"], (7, 3, width-14, 6))
        
        # Goggles on head
        pygame.draw.rect(sprite, colors["goggles"], (6, 5, width-12, 3))
        pygame.draw.circle(sprite, (200, 200, 200), (9, 6), 3)
        pygame.draw.circle(sprite, (200, 200, 200), (width-9, 6), 3)
        
        # Head (tall, so slightly elongated)
        pygame.draw.rect(sprite, colors["skin"], (7, 8, width-14, 12))
        
        # Eyes
        pygame.draw.rect(sprite, (255, 255, 255), (9, 11, 3, 2))
        pygame.draw.rect(sprite, (255, 255, 255), (width-12, 11, 3, 2))
        pygame.draw.rect(sprite, colors["eyes"], (10, 11, 1, 2))
        pygame.draw.rect(sprite, colors["eyes"], (width-11, 11, 1, 2))
        
        # Big smile
        pygame.draw.arc(sprite, (255, 100, 100), 
                       pygame.Rect(9, 14, width-18, 6), 0, 3.14, 2)
        
        # Blue work shirt
        pygame.draw.rect(sprite, colors["shirt"], (6, 20, width-12, 13))
        
        # Tool belt
        pygame.draw.rect(sprite, colors["belt"], (5, 28, width-10, 3))
        # Tools
        pygame.draw.rect(sprite, (150, 150, 150), (7, 27, 2, 4))
        pygame.draw.rect(sprite, (200, 100, 0), (11, 27, 2, 4))
        
        # Arms (tall person, longer arms)
        pygame.draw.rect(sprite, colors["skin"], (3, 21, 3, 11))
        pygame.draw.rect(sprite, colors["skin"], (width-6, 21, 3, 11))
        
        # Legs (tall)
        pygame.draw.rect(sprite, (100, 100, 150), (8, 33, 5, 7))
        pygame.draw.rect(sprite, (100, 100, 150), (width-13, 33, 5, 7))
    
    def _draw_xeno(self, sprite: pygame.Surface, colors: Dict, width: int, height: int):
        """Draw Xeno (Xenofon) - short Greek manager with glasses and spiky hair."""
        # Spiky black hair
        for i in range(5):
            x = 7 + i * 4
            # Draw spikes
            pygame.draw.polygon(sprite, colors["hair"], [
                (x, 8), (x+2, 3), (x+4, 8)
            ])
        
        # Head (shorter character)
        pygame.draw.rect(sprite, colors["skin"], (7, 8, width-14, 9))
        
        # Glasses (round frames)
        pygame.draw.circle(sprite, colors["glasses"], (10, 11), 3, 1)
        pygame.draw.circle(sprite, colors["glasses"], (width-10, 11), 3, 1)
        pygame.draw.line(sprite, colors["glasses"], (13, 11), (width-13, 11), 1)
        
        # Friendly eyes behind glasses
        pygame.draw.circle(sprite, colors["eyes"], (10, 11), 1)
        pygame.draw.circle(sprite, colors["eyes"], (width-10, 11), 1)
        
        # Calming smile
        pygame.draw.arc(sprite, (200, 100, 100),
                       pygame.Rect(8, 13, width-16, 4), 0, 3.14, 2)
        
        # Blue shirt (manager attire)
        pygame.draw.rect(sprite, colors["shirt"], (6, 17, width-12, 12))
        # Collar
        pygame.draw.polygon(sprite, (80, 130, 180), [
            (8, 17), (width//2, 19), (width-8, 17)
        ])
        
        # Arms (short character, normal proportions)
        pygame.draw.rect(sprite, colors["shirt"], (3, 18, 3, 9))
        pygame.draw.rect(sprite, colors["shirt"], (width-6, 18, 3, 9))
        
        # Hands
        pygame.draw.rect(sprite, colors["skin"], (3, 27, 3, 3))
        pygame.draw.rect(sprite, colors["skin"], (width-6, 27, 3, 3))
        
        # Pants (shorter legs)
        pygame.draw.rect(sprite, colors["pants"], (8, 29, 5, 11))
        pygame.draw.rect(sprite, colors["pants"], (width-13, 29, 5, 11))
    
    def _draw_vitalia(self, sprite: pygame.Surface, colors: Dict, width: int, height: int):
        """Draw Vitalia the health expert."""
        # Hair
        pygame.draw.rect(sprite, colors["hair"], (6, 3, width-12, 8))
        
        # Head
        pygame.draw.rect(sprite, colors["skin"], (7, 9, width-14, 10))
        
        # Caring eyes
        pygame.draw.rect(sprite, (255, 255, 255), (9, 12, 3, 2))
        pygame.draw.rect(sprite, (255, 255, 255), (width-12, 12, 3, 2))
        pygame.draw.rect(sprite, colors["eyes"], (10, 12, 1, 2))
        pygame.draw.rect(sprite, colors["eyes"], (width-11, 12, 1, 2))
        
        # Warm smile
        pygame.draw.arc(sprite, (255, 150, 150), 
                       pygame.Rect(10, 15, width-20, 4), 0, 3.14, 1)
        
        # Green scrubs
        pygame.draw.rect(sprite, colors["scrubs"], (6, 19, width-12, 15))
        
        # Medical cross
        pygame.draw.rect(sprite, (255, 255, 255), (width//2-1, 23, 2, 6))
        pygame.draw.rect(sprite, (255, 255, 255), (width//2-3, 25, 6, 2))
        
        # Stethoscope
        pygame.draw.arc(sprite, colors["stethoscope"], 
                       pygame.Rect(8, 19, width-16, 8), 0, 3.14, 2)
        
        # Arms
        pygame.draw.rect(sprite, colors["skin"], (3, 21, 3, 10))
        pygame.draw.rect(sprite, colors["skin"], (width-6, 21, 3, 10))
        
        # Legs
        pygame.draw.rect(sprite, colors["scrubs"], (8, 34, 5, 6))
        pygame.draw.rect(sprite, colors["scrubs"], (width-13, 34, 5, 6))
    
    def _draw_vitaly(self, sprite: pygame.Surface, colors: Dict, width: int, height: int):
        """Draw Vitaly the construction worker."""
        # Yellow hard hat
        pygame.draw.rect(sprite, colors["hardhat"], (6, 2, width-12, 6))
        pygame.draw.rect(sprite, (200, 200, 0), (5, 6, width-10, 2))
        
        # Head
        pygame.draw.rect(sprite, colors["skin"], (7, 8, width-14, 11))
        
        # Eyes
        pygame.draw.rect(sprite, (255, 255, 255), (9, 11, 3, 2))
        pygame.draw.rect(sprite, (255, 255, 255), (width-12, 11, 3, 2))
        pygame.draw.rect(sprite, colors["eyes"], (10, 11, 1, 2))
        pygame.draw.rect(sprite, colors["eyes"], (width-11, 11, 1, 2))
        
        # Determined expression
        pygame.draw.line(sprite, (100, 50, 0), (9, 10), (11, 10), 1)
        pygame.draw.line(sprite, (100, 50, 0), (width-11, 10), (width-9, 10), 1)
        
        # Brown work clothes
        pygame.draw.rect(sprite, colors["clothes"], (6, 19, width-12, 15))
        
        # Tool belt details
        pygame.draw.rect(sprite, (80, 40, 0), (5, 28, width-10, 3))
        pygame.draw.rect(sprite, (150, 150, 150), (7, 27, 2, 4))
        pygame.draw.rect(sprite, (200, 200, 0), (11, 27, 2, 4))
        pygame.draw.rect(sprite, (100, 100, 100), (15, 27, 2, 4))
        
        # Strong arms
        pygame.draw.rect(sprite, colors["skin"], (2, 20, 4, 11))
        pygame.draw.rect(sprite, colors["skin"], (width-6, 20, 4, 11))
        
        # Work boots
        pygame.draw.rect(sprite, colors["boots"], (7, 34, 6, 6))
        pygame.draw.rect(sprite, colors["boots"], (width-13, 34, 6, 6))
    
    def _draw_xenia(self, sprite: pygame.Surface, colors: Dict, width: int, height: int):
        """Draw Xenia the artist."""
        # Beret
        pygame.draw.ellipse(sprite, colors["beret"], pygame.Rect(6, 2, width-12, 6))
        
        # Hair
        pygame.draw.rect(sprite, colors["hair"], (5, 6, width-10, 8))
        
        # Head
        pygame.draw.rect(sprite, colors["skin"], (7, 10, width-14, 10))
        
        # Expressive eyes
        pygame.draw.rect(sprite, (255, 255, 255), (9, 13, 3, 3))
        pygame.draw.rect(sprite, (255, 255, 255), (width-12, 13, 3, 3))
        pygame.draw.rect(sprite, colors["eyes"], (10, 14, 1, 1))
        pygame.draw.rect(sprite, (100, 200, 100), (width-11, 14, 1, 1))
        
        # Colorful clothes (animated)
        if isinstance(colors["clothes"], list):
            color = random.choice(colors["clothes"])
        else:
            color = colors["clothes"]
        pygame.draw.rect(sprite, color, (6, 20, width-12, 14))
        
        # Paint splatter effect
        for _ in range(5):
            x = random.randint(7, width-8)
            y = random.randint(21, 32)
            paint_color = random.choice([(255, 100, 100), (100, 255, 100), (100, 100, 255)])
            pygame.draw.rect(sprite, paint_color, (x, y, 2, 2))
        
        # Arms
        pygame.draw.rect(sprite, colors["skin"], (3, 21, 3, 10))
        pygame.draw.rect(sprite, colors["skin"], (width-6, 21, 3, 10))
        
        # Paintbrush in hand
        pygame.draw.rect(sprite, (139, 69, 19), (width-5, 29, 1, 4))
        pygame.draw.rect(sprite, (255, 0, 0), (width-5, 28, 2, 2))
        
        # Legs
        pygame.draw.rect(sprite, (100, 100, 100), (8, 34, 5, 6))
        pygame.draw.rect(sprite, (100, 100, 100), (width-13, 34, 5, 6))
    
    def _draw_cindy(self, sprite: pygame.Surface, colors: Dict, width: int, height: int):
        """Draw Cindy the engineer."""
        # Orange hard hat
        pygame.draw.rect(sprite, colors["hardhat"], (6, 2, width-12, 5))
        
        # Hair
        pygame.draw.rect(sprite, colors["hair"], (6, 6, width-12, 6))
        
        # Head
        pygame.draw.rect(sprite, colors["skin"], (7, 10, width-14, 10))
        
        # Smart eyes
        pygame.draw.rect(sprite, (255, 255, 255), (9, 13, 3, 2))
        pygame.draw.rect(sprite, (255, 255, 255), (width-12, 13, 3, 2))
        pygame.draw.rect(sprite, colors["eyes"], (10, 13, 1, 2))
        pygame.draw.rect(sprite, colors["eyes"], (width-11, 13, 1, 2))
        
        # Orange shirt
        pygame.draw.rect(sprite, colors["shirt"], (6, 20, width-12, 10))
        
        # Safety vest
        pygame.draw.rect(sprite, colors["vest"], (5, 22, width-10, 8))
        # Reflective stripes
        pygame.draw.rect(sprite, (255, 255, 255), (5, 24, width-10, 1))
        pygame.draw.rect(sprite, (255, 255, 255), (5, 27, width-10, 1))
        
        # Clipboard in hand
        pygame.draw.rect(sprite, (255, 255, 255), (3, 26, 5, 7))
        pygame.draw.rect(sprite, (0, 0, 0), (3, 26, 5, 7), 1)
        pygame.draw.line(sprite, (0, 0, 0), (4, 28), (6, 28), 1)
        pygame.draw.line(sprite, (0, 0, 0), (4, 30), (6, 30), 1)
        
        # Arms
        pygame.draw.rect(sprite, colors["skin"], (3, 21, 3, 10))
        pygame.draw.rect(sprite, colors["skin"], (width-6, 21, 3, 10))
        
        # Legs
        pygame.draw.rect(sprite, (100, 100, 150), (8, 30, 5, 10))
        pygame.draw.rect(sprite, (100, 100, 150), (width-13, 30, 5, 10))
    
    def _draw_laurence(self, sprite: pygame.Surface, colors: Dict, width: int, height: int):
        """Draw Laurence the investor."""
        # Hair (distinguished gray)
        pygame.draw.rect(sprite, colors["hair"], (7, 3, width-14, 6))
        
        # Head
        pygame.draw.rect(sprite, colors["skin"], (7, 8, width-14, 11))
        
        # Glasses
        pygame.draw.circle(sprite, colors["glasses"], (10, 12), 3, 1)
        pygame.draw.circle(sprite, colors["glasses"], (width-10, 12), 3, 1)
        pygame.draw.line(sprite, colors["glasses"], (13, 12), (width-13, 12), 1)
        
        # Eyes behind glasses
        pygame.draw.rect(sprite, colors["eyes"], (10, 12, 1, 1))
        pygame.draw.rect(sprite, colors["eyes"], (width-10, 12, 1, 1))
        
        # Professional expression
        
        # Dark green suit
        pygame.draw.rect(sprite, colors["suit"], (6, 19, width-12, 16))
        
        # Red tie
        pygame.draw.rect(sprite, colors["tie"], (width//2-1, 20, 2, 8))
        
        # Suit jacket details
        pygame.draw.line(sprite, (30, 60, 30), (width//2, 20), (width//2, 33), 1)
        pygame.draw.rect(sprite, (30, 60, 30), (7, 22, 2, 2))
        pygame.draw.rect(sprite, (30, 60, 30), (width-9, 22, 2, 2))
        
        # Arms
        pygame.draw.rect(sprite, colors["suit"], (3, 21, 3, 11))
        pygame.draw.rect(sprite, colors["suit"], (width-6, 21, 3, 11))
        
        # Briefcase in hand
        pygame.draw.rect(sprite, (50, 30, 20), (width-5, 28, 6, 5))
        pygame.draw.rect(sprite, (0, 0, 0), (width-5, 28, 6, 5), 1)
        
        # Legs
        pygame.draw.rect(sprite, colors["suit"], (8, 35, 5, 5))
        pygame.draw.rect(sprite, colors["suit"], (width-13, 35, 5, 5))
    
    def _draw_morgan(self, sprite: pygame.Surface, colors: Dict, width: int, height: int):
        """Draw Morgan - tall, thin, bald biotech researcher."""
        # Bald head (elongated for tall character)
        pygame.draw.ellipse(sprite, colors["scalp"], pygame.Rect(7, 2, width-14, 12))
        pygame.draw.rect(sprite, colors["scalp"], (7, 7, width-14, 8))
        
        # Head shine (bald effect)
        pygame.draw.ellipse(sprite, (255, 255, 255), pygame.Rect(10, 4, 4, 3))
        
        # Intense scientific eyes
        pygame.draw.rect(sprite, (255, 255, 255), (9, 10, 3, 2))
        pygame.draw.rect(sprite, (255, 255, 255), (width-12, 10, 3, 2))
        pygame.draw.rect(sprite, colors["eyes"], (10, 10, 1, 2))
        pygame.draw.rect(sprite, colors["eyes"], (width-11, 10, 1, 2))
        
        # Thin mouth saying "Let's scan your brain"
        pygame.draw.line(sprite, (150, 50, 50), (10, 14), (width-10, 14), 1)
        
        # Lab coat (longer for tall character)
        pygame.draw.rect(sprite, colors["coat"], (4, 16, width-8, 20))
        pygame.draw.rect(sprite, (0, 0, 0), (4, 16, width-8, 20), 1)
        
        # Green shirt underneath
        pygame.draw.rect(sprite, colors["shirt"], (8, 20, width-16, 8))
        
        # DNA helix on coat
        for i in range(3):
            y = 24 + i * 3
            pygame.draw.circle(sprite, (0, 200, 0), (width//2-2, y), 1)
            pygame.draw.circle(sprite, (0, 0, 200), (width//2+2, y), 1)
        
        # Thin arms (elongated)
        pygame.draw.rect(sprite, colors["coat"], (1, 17, 2, 14))
        pygame.draw.rect(sprite, colors["coat"], (width-3, 17, 2, 14))
        
        # Brain scanner device in hand
        pygame.draw.rect(sprite, (100, 100, 255), (2, 28, 4, 3))
        pygame.draw.circle(sprite, (255, 100, 100), (4, 29), 1)
        
        # Thin legs (tall character)
        pygame.draw.rect(sprite, (50, 50, 100), (9, 36, 3, 4))
        pygame.draw.rect(sprite, (50, 50, 100), (width-12, 36, 3, 4))
    
    def _draw_china(self, sprite: pygame.Surface, colors: Dict, width: int, height: int):
        """Draw China - tiny, elegant Chinese accelerator leader."""
        # Hair (sleek black bob, elegant)
        pygame.draw.ellipse(sprite, colors["hair"], pygame.Rect(6, 5, width-12, 9))
        
        # Head (smaller, delicate features)
        pygame.draw.rect(sprite, colors["skin"], (8, 10, width-16, 8))
        
        # Elegant almond-shaped eyes
        pygame.draw.ellipse(sprite, (255, 255, 255), pygame.Rect(9, 12, 4, 2))
        pygame.draw.ellipse(sprite, (255, 255, 255), pygame.Rect(width-13, 12, 4, 2))
        pygame.draw.circle(sprite, colors["eyes"], (11, 13), 1)
        pygame.draw.circle(sprite, colors["eyes"], (width-11, 13), 1)
        
        # Delicate smile
        pygame.draw.arc(sprite, (200, 100, 100), 
                       pygame.Rect(10, 14, width-20, 3), 0, 3.14, 1)
        
        # Elegant black suit (petite sizing)
        pygame.draw.rect(sprite, colors["suit"], (7, 18, width-14, 14))
        
        # Gold shirt/tie
        pygame.draw.rect(sprite, colors["shirt"], (width//2-2, 20, 4, 8))
        
        # Delicate arms
        pygame.draw.rect(sprite, colors["suit"], (4, 19, 3, 10))
        pygame.draw.rect(sprite, colors["suit"], (width-7, 19, 3, 10))
        
        # Small hands
        pygame.draw.rect(sprite, colors["skin"], (4, 28, 3, 2))
        pygame.draw.rect(sprite, colors["skin"], (width-7, 28, 3, 2))
        
        # Dollar sign on jacket
        pygame.draw.line(sprite, colors["shirt"], (8, 24), (8, 28), 2)
        pygame.draw.line(sprite, colors["shirt"], (7, 24), (9, 24), 1)
        pygame.draw.line(sprite, colors["shirt"], (7, 26), (9, 26), 1)
        pygame.draw.line(sprite, colors["shirt"], (7, 28), (9, 28), 1)
        
        # Petite legs
        pygame.draw.rect(sprite, colors["suit"], (9, 32, 4, 8))
        pygame.draw.rect(sprite, colors["suit"], (width-13, 32, 4, 8))
    
    def _draw_devinder(self, sprite: pygame.Surface, colors: Dict, width: int, height: int):
        """Draw Devinder - tall, handsome Indian AI researcher."""
        # Styled black hair
        pygame.draw.rect(sprite, colors["hair"], (6, 2, width-12, 7))
        # Hair wave detail
        pygame.draw.arc(sprite, (10, 10, 10), 
                       pygame.Rect(7, 2, width-14, 6), 0, 3.14, 2)
        
        # Head (handsome features)
        pygame.draw.rect(sprite, colors["skin"], (7, 8, width-14, 11))
        
        # Handsome eyes with depth
        pygame.draw.rect(sprite, (255, 255, 255), (9, 11, 4, 3))
        pygame.draw.rect(sprite, (255, 255, 255), (width-13, 11, 4, 3))
        pygame.draw.rect(sprite, colors["eyes"], (10, 12, 2, 2))
        pygame.draw.rect(sprite, colors["eyes"], (width-12, 12, 2, 2))
        # Eye sparkle
        pygame.draw.rect(sprite, (255, 255, 255), (10, 12, 1, 1))
        pygame.draw.rect(sprite, (255, 255, 255), (width-11, 12, 1, 1))
        
        # Confident smile
        pygame.draw.arc(sprite, (150, 50, 50), 
                       pygame.Rect(9, 15, width-18, 4), 0, 3.14, 2)
        
        # Futuristic blue tech wear
        pygame.draw.rect(sprite, colors["clothes"], (6, 19, width-12, 15))
        
        # Cyan accent lines (tech style)
        pygame.draw.line(sprite, colors["accent"], (6, 21), (6, 32), 2)
        pygame.draw.line(sprite, colors["accent"], (width-6, 21), (width-6, 32), 2)
        pygame.draw.line(sprite, colors["accent"], (8, 26), (width-8, 26), 1)
        
        # AI neural network pattern on chest
        for i in range(3):
            for j in range(2):
                x = 10 + i * 4
                y = 23 + j * 4
                pygame.draw.circle(sprite, colors["accent"], (x, y), 1)
                if i < 2:
                    pygame.draw.line(sprite, colors["accent"], (x, y), (x+4, y), 1)
                if j < 1:
                    pygame.draw.line(sprite, colors["accent"], (x, y), (x+2, y+4), 1)
        
        # Strong arms (tall build)
        pygame.draw.rect(sprite, colors["clothes"], (2, 20, 4, 13))
        pygame.draw.rect(sprite, colors["clothes"], (width-6, 20, 4, 13))
        
        # Holographic tablet in hand
        pygame.draw.rect(sprite, (100, 200, 255), (width-6, 27, 5, 3))
        pygame.draw.rect(sprite, (255, 255, 255), (width-5, 28, 3, 1))
        
        # Long legs (tall character)
        pygame.draw.rect(sprite, colors["clothes"], (8, 33, 5, 7))
        pygame.draw.rect(sprite, colors["clothes"], (width-13, 33, 5, 7))
    
    def _draw_headphone_james(self, sprite: pygame.Surface, colors: Dict, width: int, height: int):
        """Draw Headphone James - the mysterious hero who saves the day."""
        # Hair
        pygame.draw.rect(sprite, colors["hair"], (7, 4, width-14, 6))
        
        # Huge headphones (his signature)
        pygame.draw.arc(sprite, colors["headphones"], 
                       pygame.Rect(4, 1, width-8, 12), 0, 3.14, 4)
        # Ear cups
        pygame.draw.circle(sprite, colors["headphones"], (6, 8), 5)
        pygame.draw.circle(sprite, colors["headphones"], (width-6, 8), 5)
        # Headphone details
        pygame.draw.circle(sprite, (200, 30, 30), (6, 8), 3)
        pygame.draw.circle(sprite, (200, 30, 30), (width-6, 8), 3)
        
        # Head
        pygame.draw.rect(sprite, colors["skin"], (7, 9, width-14, 10))
        
        # Cool eyes
        pygame.draw.rect(sprite, (255, 255, 255), (9, 12, 3, 2))
        pygame.draw.rect(sprite, (255, 255, 255), (width-12, 12, 3, 2))
        pygame.draw.rect(sprite, colors["eyes"], (10, 12, 1, 2))
        pygame.draw.rect(sprite, colors["eyes"], (width-11, 12, 1, 2))
        
        # Confident smirk
        pygame.draw.arc(sprite, (150, 50, 50), 
                       pygame.Rect(10, 15, width-20, 3), 0.5, 2.5, 2)
        
        # Hero cape (flowing behind)
        pygame.draw.polygon(sprite, colors["cape"], [
            (5, 20), (3, 38), (8, 35), (10, 20)
        ])
        pygame.draw.polygon(sprite, colors["cape"], [
            (width-5, 20), (width-3, 38), (width-8, 35), (width-10, 20)
        ])
        
        # Tie-dye shirt (psychedelic colors)
        if "tiedye" in colors:
            # Create tie-dye pattern
            for y in range(19, 32, 2):
                for x in range(6, width-6, 3):
                    color_index = ((x + y) // 5) % len(colors["tiedye"])
                    pygame.draw.rect(sprite, colors["tiedye"][color_index], (x, y, 3, 2))
        else:
            pygame.draw.rect(sprite, (200, 100, 200), (6, 19, width-12, 13))
        
        # Hero emblem (music note)
        pygame.draw.circle(sprite, (255, 255, 255), (width//2, 25), 3)
        pygame.draw.line(sprite, (255, 255, 255), (width//2+3, 25), (width//2+3, 22), 2)
        pygame.draw.line(sprite, (255, 255, 255), (width//2+3, 22), (width//2+5, 23), 1)
        
        # Arms
        pygame.draw.rect(sprite, colors["skin"], (3, 21, 3, 10))
        pygame.draw.rect(sprite, colors["skin"], (width-6, 21, 3, 10))
        
        # Pants
        pygame.draw.rect(sprite, colors["pants"], (8, 32, 5, 8))
        pygame.draw.rect(sprite, colors["pants"], (width-13, 32, 5, 8))
    
    def _draw_generic(self, sprite: pygame.Surface, width: int, height: int):
        """Draw a generic NPC sprite."""
        # Simple body
        color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        pygame.draw.rect(sprite, color, (5, 5, width-10, height-10))
        pygame.draw.rect(sprite, (0, 0, 0), (5, 5, width-10, height-10), 1)
        
        # Simple eyes
        pygame.draw.circle(sprite, (255, 255, 255), (10, 15), 2)
        pygame.draw.circle(sprite, (255, 255, 255), (width-10, 15), 2)
        pygame.draw.circle(sprite, (0, 0, 0), (10, 15), 1)
        pygame.draw.circle(sprite, (0, 0, 0), (width-10, 15), 1)


# Singleton instance
_sprite_generator = None

def get_sprite_generator():
    """Get the singleton sprite generator instance."""
    global _sprite_generator
    if _sprite_generator is None:
        _sprite_generator = AISpritGenerator()
    return _sprite_generator
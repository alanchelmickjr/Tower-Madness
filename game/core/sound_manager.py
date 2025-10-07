"""
Sound management system for Tower Madness
Handles all audio playback including SFX and music
"""

import pygame
from typing import Dict, Optional
from game.core.sound_generator import SoundGenerator

class SoundManager:
    """Manages all game audio including sound effects and music."""
    
    _instance = None  # Singleton instance
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(SoundManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self):
        """Initialize the sound manager."""
        if self._initialized:
            return
            
        self._initialized = True
        self.enabled = True
        self.sfx_enabled = True
        self.music_enabled = True
        
        # Volume settings (0.0 to 1.0)
        self.master_volume = 0.8
        self.sfx_volume = 0.9
        self.music_volume = 0.7
        
        # Sound library
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.generator = SoundGenerator()
        
        # Music state
        self.current_music = None
        self.music_tracks: Dict[str, str] = {}
        
        # Initialize pygame mixer if not already done
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self._generate_sounds()
        except Exception as e:
            print(f"Warning: Could not initialize audio: {e}")
            self.enabled = False
            
    def _generate_sounds(self):
        """Generate all game sound effects."""
        if not self.enabled:
            return
            
        try:
            print("Generating 8-bit sound effects...")
            
            # Elevator sounds
            self.sounds['elevator_start'] = self.generator.generate_elevator_move(0.25)
            self.sounds['elevator_stop'] = self.generator.generate_ding(0.3)
            self.sounds['elevator_ding'] = self.generator.generate_ding(0.35)
            
            # Door sounds
            self.sounds['doors_open'] = self.generator.generate_door_sound(opening=True, volume=0.25)
            self.sounds['doors_close'] = self.generator.generate_door_sound(opening=False, volume=0.25)
            
            # NPC sounds
            self.sounds['npc_enter'] = self.generator.generate_pickup(0.3)
            self.sounds['npc_exit'] = self.generator.generate_tone(600, 0.1, 'square', 0.25)
            self.sounds['npc_delivered'] = self.generator.generate_delivery(0.3)
            self.sounds['npc_angry'] = self.generator.generate_warning(0.25)
            self.sounds['special_npc'] = self.generator.generate_sweep(400, 1200, 0.3, 'sine', 0.3)
            
            # Scoring sounds
            self.sounds['score_points'] = self.generator.generate_tone(800, 0.1, 'square', 0.25)
            self.sounds['bonus_score'] = self.generator.generate_sweep(600, 1200, 0.2, 'square', 0.3)
            self.sounds['high_score'] = self.generator.generate_high_score(0.35)
            
            # Disaster sounds
            self.sounds['flood_warning'] = self.generator.generate_warning(0.3)
            self.sounds['disaster_start'] = self.generator.generate_explosion(0.5, 0.25)
            self.sounds['chaos_rising'] = self.generator.generate_sweep(200, 100, 0.5, 'sawtooth', 0.2)
            
            # Game state sounds
            self.sounds['game_start'] = self.generator.generate_sweep(200, 800, 0.5, 'square', 0.3)
            self.sounds['game_over'] = self.generator.generate_game_over(0.3)
            self.sounds['pause'] = self.generator.generate_tone(440, 0.2, 'square', 0.25)
            self.sounds['menu_select'] = self.generator.generate_tone(600, 0.1, 'square', 0.25)
            self.sounds['menu_move'] = self.generator.generate_tone(400, 0.05, 'square', 0.2)
            
            print(f"Generated {len(self.sounds)} sound effects!")
            
        except Exception as e:
            print(f"Error generating sounds: {e}")
            self.enabled = False
            
    def play_sfx(self, sound_name: str, volume: Optional[float] = None):
        """Play a sound effect.
        
        Args:
            sound_name: Name of the sound to play
            volume: Optional volume override (0.0 to 1.0)
        """
        if not self.enabled or not self.sfx_enabled:
            return
            
        if sound_name not in self.sounds:
            print(f"Warning: Sound '{sound_name}' not found")
            return
            
        try:
            sound = self.sounds[sound_name]
            if volume is not None:
                sound.set_volume(volume * self.sfx_volume * self.master_volume)
            else:
                sound.set_volume(self.sfx_volume * self.master_volume)
            sound.play()
        except Exception as e:
            print(f"Error playing sound '{sound_name}': {e}")
            
    def play_music(self, track_name: str, loop: bool = True, fade_ms: int = 1000):
        """Play background music.
        
        Args:
            track_name: Name of the music track
            loop: Whether to loop the music
            fade_ms: Fade in time in milliseconds
        """
        if not self.enabled or not self.music_enabled:
            return
            
        # For now, we'll use generated tones as placeholder music
        # In a full implementation, you'd load actual music files here
        try:
            if self.current_music != track_name:
                pygame.mixer.music.stop()
                self.current_music = track_name
                # Placeholder: would load actual music file here
                # pygame.mixer.music.load(track_file)
                # pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
                # pygame.mixer.music.play(-1 if loop else 0, fade_ms=fade_ms)
        except Exception as e:
            print(f"Error playing music '{track_name}': {e}")
            
    def stop_music(self, fade_ms: int = 1000):
        """Stop background music.
        
        Args:
            fade_ms: Fade out time in milliseconds
        """
        if not self.enabled:
            return
            
        try:
            pygame.mixer.music.fadeout(fade_ms)
            self.current_music = None
        except Exception as e:
            print(f"Error stopping music: {e}")
            
    def set_master_volume(self, volume: float):
        """Set master volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.master_volume = max(0.0, min(1.0, volume))
        if self.enabled:
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
            
    def set_sfx_volume(self, volume: float):
        """Set sound effects volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.sfx_volume = max(0.0, min(1.0, volume))
        
    def set_music_volume(self, volume: float):
        """Set music volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        if self.enabled:
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
            
    def toggle_sfx(self):
        """Toggle sound effects on/off."""
        self.sfx_enabled = not self.sfx_enabled
        
    def toggle_music(self):
        """Toggle music on/off."""
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            self.stop_music()
            
    def toggle_all(self):
        """Toggle all audio on/off."""
        self.enabled = not self.enabled
        if not self.enabled:
            self.stop_music()
            
    def preload_sounds(self):
        """Preload all sounds (already done in __init__)."""
        if not self.enabled:
            return
        # Sounds are generated in _generate_sounds() during init
        pass
        
    def get_sound(self, sound_name: str) -> Optional[pygame.mixer.Sound]:
        """Get a sound object by name.
        
        Args:
            sound_name: Name of the sound
            
        Returns:
            pygame.mixer.Sound object or None if not found
        """
        return self.sounds.get(sound_name)
        
    def is_enabled(self) -> bool:
        """Check if audio system is enabled.
        
        Returns:
            True if audio is enabled and working
        """
        return self.enabled
        
    def get_status(self) -> Dict[str, any]:
        """Get current audio system status.
        
        Returns:
            Dictionary with status information
        """
        return {
            'enabled': self.enabled,
            'sfx_enabled': self.sfx_enabled,
            'music_enabled': self.music_enabled,
            'master_volume': self.master_volume,
            'sfx_volume': self.sfx_volume,
            'music_volume': self.music_volume,
            'current_music': self.current_music,
            'sounds_loaded': len(self.sounds)
        }


# Global singleton instance
_sound_manager_instance = None

def get_sound_manager() -> SoundManager:
    """Get the global sound manager instance.
    
    Returns:
        SoundManager singleton instance
    """
    global _sound_manager_instance
    if _sound_manager_instance is None:
        _sound_manager_instance = SoundManager()
    return _sound_manager_instance
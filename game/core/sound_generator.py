"""
Procedural 8-bit sound generation for Tower Madness
Generates retro arcade sounds using simple waveforms
"""

import pygame
import numpy as np
import math

class SoundGenerator:
    """Generates 8-bit style sound effects procedurally."""
    
    def __init__(self, sample_rate: int = 22050):
        """Initialize the sound generator.
        
        Args:
            sample_rate: Audio sample rate in Hz
        """
        self.sample_rate = sample_rate
        
    def generate_tone(self, frequency: float, duration: float, 
                     wave_type: str = 'square', volume: float = 0.3) -> pygame.mixer.Sound:
        """Generate a simple tone.
        
        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds
            wave_type: 'square', 'sine', 'triangle', or 'sawtooth'
            volume: Volume (0.0 to 1.0)
            
        Returns:
            pygame.mixer.Sound object
        """
        num_samples = int(self.sample_rate * duration)
        samples = np.zeros(num_samples, dtype=np.int16)
        
        for i in range(num_samples):
            t = i / self.sample_rate
            
            if wave_type == 'square':
                value = 1.0 if math.sin(2 * math.pi * frequency * t) > 0 else -1.0
            elif wave_type == 'sine':
                value = math.sin(2 * math.pi * frequency * t)
            elif wave_type == 'triangle':
                value = 2.0 * abs(2.0 * (t * frequency - math.floor(t * frequency + 0.5))) - 1.0
            elif wave_type == 'sawtooth':
                value = 2.0 * (t * frequency - math.floor(t * frequency + 0.5))
            else:
                value = 0.0
                
            samples[i] = int(value * volume * 32767)
            
        # Convert to stereo
        stereo_samples = np.column_stack((samples, samples))
        return pygame.sndarray.make_sound(stereo_samples)
        
    def generate_sweep(self, start_freq: float, end_freq: float, duration: float,
                      wave_type: str = 'square', volume: float = 0.3) -> pygame.mixer.Sound:
        """Generate a frequency sweep (slide).
        
        Args:
            start_freq: Starting frequency in Hz
            end_freq: Ending frequency in Hz
            duration: Duration in seconds
            wave_type: Waveform type
            volume: Volume (0.0 to 1.0)
            
        Returns:
            pygame.mixer.Sound object
        """
        num_samples = int(self.sample_rate * duration)
        samples = np.zeros(num_samples, dtype=np.int16)
        
        for i in range(num_samples):
            t = i / self.sample_rate
            progress = t / duration
            frequency = start_freq + (end_freq - start_freq) * progress
            
            if wave_type == 'square':
                value = 1.0 if math.sin(2 * math.pi * frequency * t) > 0 else -1.0
            elif wave_type == 'sine':
                value = math.sin(2 * math.pi * frequency * t)
            else:
                value = math.sin(2 * math.pi * frequency * t)
                
            # Apply envelope (fade out)
            envelope = 1.0 - (progress * 0.5)
            samples[i] = int(value * volume * envelope * 32767)
            
        stereo_samples = np.column_stack((samples, samples))
        return pygame.sndarray.make_sound(stereo_samples)
        
    def generate_noise(self, duration: float, volume: float = 0.2) -> pygame.mixer.Sound:
        """Generate white noise.
        
        Args:
            duration: Duration in seconds
            volume: Volume (0.0 to 1.0)
            
        Returns:
            pygame.mixer.Sound object
        """
        num_samples = int(self.sample_rate * duration)
        samples = np.random.randint(-32767, 32767, num_samples, dtype=np.int16)
        samples = (samples * volume).astype(np.int16)
        
        stereo_samples = np.column_stack((samples, samples))
        return pygame.sndarray.make_sound(stereo_samples)
        
    def generate_explosion(self, duration: float = 0.5, volume: float = 0.3) -> pygame.mixer.Sound:
        """Generate an explosion sound effect.
        
        Args:
            duration: Duration in seconds
            volume: Volume (0.0 to 1.0)
            
        Returns:
            pygame.mixer.Sound object
        """
        num_samples = int(self.sample_rate * duration)
        samples = np.zeros(num_samples, dtype=np.int16)
        
        for i in range(num_samples):
            t = i / self.sample_rate
            progress = t / duration
            
            # Mix noise with low frequency rumble
            noise = np.random.random() * 2 - 1
            rumble = math.sin(2 * math.pi * 60 * t * (1 - progress))
            
            # Envelope (sharp attack, exponential decay)
            envelope = math.exp(-progress * 5)
            
            value = (noise * 0.7 + rumble * 0.3) * envelope
            samples[i] = int(value * volume * 32767)
            
        stereo_samples = np.column_stack((samples, samples))
        return pygame.sndarray.make_sound(stereo_samples)
        
    def generate_pickup(self, volume: float = 0.3) -> pygame.mixer.Sound:
        """Generate a pickup/collect sound.
        
        Args:
            volume: Volume (0.0 to 1.0)
            
        Returns:
            pygame.mixer.Sound object
        """
        return self.generate_sweep(400, 800, 0.1, 'square', volume)
        
    def generate_delivery(self, volume: float = 0.3) -> pygame.mixer.Sound:
        """Generate a delivery/success sound.
        
        Args:
            volume: Volume (0.0 to 1.0)
            
        Returns:
            pygame.mixer.Sound object
        """
        # Ascending arpeggio
        duration = 0.4
        num_samples = int(self.sample_rate * duration)
        samples = np.zeros(num_samples, dtype=np.int16)
        
        notes = [523, 659, 784, 1047]  # C, E, G, C (major chord)
        note_duration = duration / len(notes)
        
        for note_idx, freq in enumerate(notes):
            start_sample = int(note_idx * note_duration * self.sample_rate)
            end_sample = int((note_idx + 1) * note_duration * self.sample_rate)
            
            for i in range(start_sample, min(end_sample, num_samples)):
                t = i / self.sample_rate
                value = math.sin(2 * math.pi * freq * t)
                
                # Envelope
                note_progress = (i - start_sample) / (end_sample - start_sample)
                envelope = 1.0 - note_progress * 0.5
                
                samples[i] = int(value * volume * envelope * 32767)
                
        stereo_samples = np.column_stack((samples, samples))
        return pygame.sndarray.make_sound(stereo_samples)
        
    def generate_door_sound(self, opening: bool = True, volume: float = 0.25) -> pygame.mixer.Sound:
        """Generate door open/close sound.
        
        Args:
            opening: True for opening, False for closing
            volume: Volume (0.0 to 1.0)
            
        Returns:
            pygame.mixer.Sound object
        """
        if opening:
            return self.generate_sweep(200, 400, 0.3, 'triangle', volume)
        else:
            return self.generate_sweep(400, 200, 0.3, 'triangle', volume)
            
    def generate_elevator_move(self, volume: float = 0.2) -> pygame.mixer.Sound:
        """Generate elevator movement sound.
        
        Args:
            volume: Volume (0.0 to 1.0)
            
        Returns:
            pygame.mixer.Sound object
        """
        # Low rumble with slight variation
        duration = 0.5
        num_samples = int(self.sample_rate * duration)
        samples = np.zeros(num_samples, dtype=np.int16)
        
        for i in range(num_samples):
            t = i / self.sample_rate
            # Mix two low frequencies for mechanical sound
            value = (math.sin(2 * math.pi * 80 * t) + 
                    math.sin(2 * math.pi * 120 * t) * 0.5)
            samples[i] = int(value * volume * 32767)
            
        stereo_samples = np.column_stack((samples, samples))
        return pygame.sndarray.make_sound(stereo_samples)
        
    def generate_ding(self, volume: float = 0.3) -> pygame.mixer.Sound:
        """Generate elevator arrival ding.
        
        Args:
            volume: Volume (0.0 to 1.0)
            
        Returns:
            pygame.mixer.Sound object
        """
        # Two-tone ding
        duration = 0.3
        num_samples = int(self.sample_rate * duration)
        samples = np.zeros(num_samples, dtype=np.int16)
        
        # First tone
        freq1 = 800
        for i in range(num_samples // 2):
            t = i / self.sample_rate
            value = math.sin(2 * math.pi * freq1 * t)
            envelope = math.exp(-t * 10)
            samples[i] = int(value * volume * envelope * 32767)
            
        # Second tone
        freq2 = 600
        for i in range(num_samples // 2, num_samples):
            t = (i - num_samples // 2) / self.sample_rate
            value = math.sin(2 * math.pi * freq2 * t)
            envelope = math.exp(-t * 10)
            samples[i] = int(value * volume * envelope * 32767)
            
        stereo_samples = np.column_stack((samples, samples))
        return pygame.sndarray.make_sound(stereo_samples)
        
    def generate_warning(self, volume: float = 0.3) -> pygame.mixer.Sound:
        """Generate warning/alert sound.
        
        Args:
            volume: Volume (0.0 to 1.0)
            
        Returns:
            pygame.mixer.Sound object
        """
        # Alternating tones
        duration = 0.6
        num_samples = int(self.sample_rate * duration)
        samples = np.zeros(num_samples, dtype=np.int16)
        
        freq1, freq2 = 440, 330
        switch_time = 0.15
        
        for i in range(num_samples):
            t = i / self.sample_rate
            freq = freq1 if (t % (switch_time * 2)) < switch_time else freq2
            value = 1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0
            samples[i] = int(value * volume * 32767)
            
        stereo_samples = np.column_stack((samples, samples))
        return pygame.sndarray.make_sound(stereo_samples)
        
    def generate_game_over(self, volume: float = 0.3) -> pygame.mixer.Sound:
        """Generate game over sound.
        
        Args:
            volume: Volume (0.0 to 1.0)
            
        Returns:
            pygame.mixer.Sound object
        """
        # Descending sad trombone
        return self.generate_sweep(400, 100, 1.0, 'triangle', volume)
        
    def generate_high_score(self, volume: float = 0.3) -> pygame.mixer.Sound:
        """Generate high score achievement sound.
        
        Args:
            volume: Volume (0.0 to 1.0)
            
        Returns:
            pygame.mixer.Sound object
        """
        # Triumphant fanfare
        duration = 1.0
        num_samples = int(self.sample_rate * duration)
        samples = np.zeros(num_samples, dtype=np.int16)
        
        # Victory melody
        notes = [523, 659, 784, 1047, 1319]  # C, E, G, C, E (ascending)
        note_duration = duration / len(notes)
        
        for note_idx, freq in enumerate(notes):
            start_sample = int(note_idx * note_duration * self.sample_rate)
            end_sample = int((note_idx + 1) * note_duration * self.sample_rate)
            
            for i in range(start_sample, min(end_sample, num_samples)):
                t = (i - start_sample) / self.sample_rate
                value = math.sin(2 * math.pi * freq * t)
                
                # Envelope with sustain
                note_progress = (i - start_sample) / (end_sample - start_sample)
                envelope = 1.0 if note_progress < 0.7 else (1.0 - (note_progress - 0.7) / 0.3)
                
                samples[i] = int(value * volume * envelope * 32767)
                
        stereo_samples = np.column_stack((samples, samples))
        return pygame.sndarray.make_sound(stereo_samples)
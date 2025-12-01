"""Audio feedback engine - The Geiger Counter."""

import asyncio
import threading
from typing import Optional
try:
    import simpleaudio as sa
except ImportError:
    sa = None


class AudioEngine:
    """Audio feedback for log events."""
    
    def __init__(self, enabled: bool = True, volume: float = 0.5):
        self.enabled = enabled and sa is not None
        self.volume = volume
        self.error_rate = 0
        self.lock = threading.Lock()
    
    def play_tick(self):
        """Play a quiet tick sound for normal operations."""
        if not self.enabled:
            return
        # Generate a simple tick (440Hz for 50ms)
        self._play_tone(440, 0.05, 0.1)
    
    def play_error(self):
        """Play a thud sound for errors."""
        if not self.enabled:
            return
        # Generate a lower thud (220Hz for 100ms)
        self._play_tone(220, 0.1, 0.3)
    
    def play_critical(self):
        """Play a Geiger counter crackle for critical errors."""
        if not self.enabled:
            return
        # Generate a harsh crackle (random noise burst)
        self._play_tone(880, 0.03, 0.5)
    
    def _play_tone(self, frequency: int, duration: float, volume: float):
        """Generate and play a simple tone."""
        if not self.enabled:
            return
        
        try:
            import numpy as np
            sample_rate = 44100
            t = np.linspace(0, duration, int(sample_rate * duration))
            wave = np.sin(2 * np.pi * frequency * t)
            
            # Apply volume
            wave = wave * volume * self.volume
            
            # Convert to 16-bit PCM
            audio = (wave * 32767).astype(np.int16)
            
            # Play in background thread
            def play():
                play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
                play_obj.wait_done()
            
            thread = threading.Thread(target=play, daemon=True)
            thread.start()
        except Exception:
            pass  # Silently fail if audio doesn't work
    
    def process_log(self, message: str):
        """Process a log message and play appropriate sound."""
        message_lower = message.lower()
        
        if "error" in message_lower or "500" in message:
            self.play_error()
            with self.lock:
                self.error_rate += 1
        elif "critical" in message_lower or "fatal" in message_lower:
            self.play_critical()
            with self.lock:
                self.error_rate += 2
        elif "200" in message or "ok" in message_lower:
            self.play_tick()
            with self.lock:
                self.error_rate = max(0, self.error_rate - 0.5)
    
    def get_error_rate(self) -> int:
        """Get current error rate."""
        with self.lock:
            return int(self.error_rate)

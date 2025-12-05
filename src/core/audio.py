"""Audio feedback engine - The Geiger Counter."""

import io
import os
import struct
import subprocess
import threading
import wave
from typing import Optional


class AudioEngine:
    """Audio feedback for log events using system audio players."""
    
    def __init__(self, enabled: bool = True, volume: float = 0.5):
        self.enabled = enabled
        self.volume = max(0.0, min(1.0, volume))
        self.error_rate = 0
        self.lock = threading.Lock()
        self._audio_lock = threading.Lock()
        
        # Find available audio player
        self._player = self._find_player()
        if not self._player:
            self.enabled = False
    
    def _find_player(self) -> Optional[str]:
        """Find an available audio player on the system."""
        players = ['paplay', 'aplay', 'afplay']  # paplay=PulseAudio, aplay=ALSA, afplay=macOS
        for player in players:
            try:
                result = subprocess.run(
                    ['which', player],
                    capture_output=True,
                    timeout=2
                )
                if result.returncode == 0:
                    return player
            except Exception:
                continue
        return None
    
    def _generate_wav(self, samples: list[int], sample_rate: int = 22050) -> bytes:
        """Generate WAV file bytes from samples."""
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)  # 16-bit
            wav.setframerate(sample_rate)
            wav.writeframes(struct.pack(f'<{len(samples)}h', *samples))
        return buf.getvalue()
    
    def _generate_soft_tone(self, freq: float, duration: float,
                            sample_rate: int = 22050, fade: bool = True) -> list[int]:
        """Generate soft sine wave with fade in/out for a gentle sound."""
        import math
        samples = []
        num_samples = int(sample_rate * duration)
        amplitude = int(12000 * self.volume)  # Softer base amplitude
        fade_samples = int(num_samples * 0.3) if fade else 0
        
        for i in range(num_samples):
            t = i / sample_rate
            # Sine wave
            sample = amplitude * math.sin(2 * math.pi * freq * t)
            
            # Apply fade in/out envelope for smoothness
            if fade and i < fade_samples:
                sample *= i / fade_samples
            elif fade and i > num_samples - fade_samples:
                sample *= (num_samples - i) / fade_samples
            
            samples.append(int(sample))
        return samples
    
    def _generate_chime(self, base_freq: float, duration: float,
                        sample_rate: int = 22050) -> list[int]:
        """Generate a soft chime with harmonics - like a gentle bell."""
        import math
        samples = []
        num_samples = int(sample_rate * duration)
        amplitude = int(10000 * self.volume)
        
        for i in range(num_samples):
            t = i / sample_rate
            # Fundamental + soft harmonics for warmth
            sample = (
                math.sin(2 * math.pi * base_freq * t) * 1.0 +
                math.sin(2 * math.pi * base_freq * 2 * t) * 0.3 +
                math.sin(2 * math.pi * base_freq * 3 * t) * 0.1
            )
            
            # Exponential decay for natural bell-like sound
            decay = math.exp(-3 * t / duration)
            sample = int(amplitude * sample * decay)
            samples.append(sample)
        return samples
    
    def _play_samples(self, samples: list[int], sample_rate: int = 22050):
        """Play samples using system audio player."""
        if not self.enabled or not self._player:
            return
        
        # Non-blocking lock - skip if already playing
        if not self._audio_lock.acquire(blocking=False):
            return
        
        def play():
            try:
                wav_data = self._generate_wav(samples, sample_rate)
                
                # Use subprocess to play
                proc = subprocess.Popen(
                    [self._player],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                proc.communicate(input=wav_data, timeout=3)
            except Exception:
                pass
            finally:
                self._audio_lock.release()
        
        thread = threading.Thread(target=play, daemon=True)
        thread.start()
    
    def play_tick(self):
        """Play a quiet tick sound for normal operations."""
        if not self.enabled:
            return
        samples = self._generate_soft_tone(440, 0.05)
        self._play_samples(samples)
    
    def play_error(self):
        """Play a soft low tone for errors."""
        if not self.enabled:
            return
        samples = self._generate_soft_tone(220, 0.1)
        self._play_samples(samples)
    
    def play_critical(self):
        """Play a gentle alert for critical errors."""
        if not self.enabled:
            return
        samples = self._generate_chime(330, 0.15)  # E4 - lower, attention-getting
        self._play_samples(samples)
    
    def play_notification(self):
        """Play a soft, soothing notification chime for new messages."""
        if not self.enabled:
            return
        
        sample_rate = 22050
        # Gentle two-note chime - like a soft doorbell or wind chime
        # Using musical intervals (perfect fifth) for pleasing sound
        samples = self._generate_chime(523, 0.15, sample_rate)  # C5
        
        self._play_samples(samples, sample_rate)
    
    def play_dm_notification(self):
        """Play a gentle ascending chime for DM notifications."""
        if not self.enabled:
            return
        
        sample_rate = 22050
        # Soft two-note ascending chime (major third interval)
        samples = []
        samples.extend(self._generate_soft_tone(440, 0.1, sample_rate))  # A4
        samples.extend([0] * int(sample_rate * 0.05))  # Small gap
        samples.extend(self._generate_chime(554, 0.18, sample_rate))  # C#5
        
        self._play_samples(samples, sample_rate)
    
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

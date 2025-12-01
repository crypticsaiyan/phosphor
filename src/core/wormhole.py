

"""Magic Wormhole integration for peer-to-peer file transfers."""

import asyncio
import subprocess
from typing import Optional, Callable


class WormholeClient:
    """Client for Magic Wormhole file transfers."""
    
    def __init__(self):
        self.status_callback: Optional[Callable] = None
    
    async def send_file(self, filepath: str) -> str:
        """Send a file and return the wormhole code."""
        try:
            process = await asyncio.create_subprocess_exec(
                "wormhole", "send", filepath,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Read output to find the code
            code = None
            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                line_str = line.decode().strip()
                if "wormhole receive" in line_str:
                    # Extract code from line like "wormhole receive 7-guitar-ocean"
                    parts = line_str.split()
                    if len(parts) >= 3:
                        code = parts[-1]
                        break
            
            if code:
                if self.status_callback:
                    self.status_callback(f"File ready! Code: {code}")
                return code
            else:
                return "error-generating-code"
                
        except FileNotFoundError:
            if self.status_callback:
                self.status_callback("Error: wormhole not installed")
            return "wormhole-not-found"
        except Exception as e:
            if self.status_callback:
                self.status_callback(f"Error: {str(e)}")
            return "error"
    
    async def receive_file(self, code: str, output_dir: str = ".") -> bool:
        """Receive a file using a wormhole code."""
        try:
            process = await asyncio.create_subprocess_exec(
                "wormhole", "receive", code,
                cwd=output_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            await process.wait()
            
            if process.returncode == 0:
                if self.status_callback:
                    self.status_callback(f"File received successfully!")
                return True
            else:
                if self.status_callback:
                    self.status_callback(f"Failed to receive file")
                return False
                
        except FileNotFoundError:
            if self.status_callback:
                self.status_callback("Error: wormhole not installed")
            return False
        except Exception as e:
            if self.status_callback:
                self.status_callback(f"Error: {str(e)}")
            return False
    
    def set_status_callback(self, callback: Callable):
        """Set callback for status updates."""
        self.status_callback = callback

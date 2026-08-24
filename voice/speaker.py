import os
import platform
import re
import subprocess
import threading
from typing import Optional


class Speaker:
    """Text-to-Speech engine utilizing native macOS speech capabilities."""

    def __init__(self, voice: str = "Daniel", rate: int = 185, enabled: bool = True):
        self.voice = voice
        self.rate = rate
        self.enabled = enabled
        self._current_process: Optional[subprocess.Popen] = None
        self._lock = threading.Lock()

    def clean_text_for_speech(self, text: str) -> str:
        """Removes markdown syntax, URLs, and code blocks for natural-sounding speech."""
        if not text:
            return ""

        # Remove code blocks ``` ... ```
        cleaned = re.sub(r'```[\s\S]*?```', 'code block omitted', text)
        
        # Remove inline code `code`
        cleaned = re.sub(r'`([^`]+)`', r'\1', cleaned)
        
        # Remove Markdown links [text](url) -> text
        cleaned = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', cleaned)
        
        # Remove markdown bold/italic asterisks and underscores
        cleaned = re.sub(r'[*_~#>-]', ' ', cleaned)
        
        # Collapse multiple whitespaces and newlines
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    def stop(self):
        """Stops any currently playing speech."""
        with self._lock:
            if self._current_process and self._current_process.poll() is None:
                try:
                    self._current_process.terminate()
                except Exception:
                    pass
                self._current_process = None

    def speak(self, text: str, wait: bool = True):
        """Speaks the provided text aloud.
        
        Args:
            text: The message string to speak.
            wait: If True, blocks until speech finishes. If False, speaks in background.
        """
        if not self.enabled:
            return

        speech_text = self.clean_text_for_speech(text)
        if not speech_text:
            return

        # Stop previous speech if any
        self.stop()

        if platform.system() == "Darwin":
            try:
                cmd = ["say", "-v", self.voice, "-r", str(self.rate), speech_text]
                if wait:
                    subprocess.run(cmd, check=False)
                else:
                    with self._lock:
                        self._current_process = subprocess.Popen(cmd)
            except Exception as e:
                print(f" [Voice Warning] TTS Error: {e}")
        else:
            # Fallback for non-macOS if ever needed
            pass

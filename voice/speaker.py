import asyncio
import os
import platform
import re
import subprocess
import tempfile
import threading
from typing import Optional

try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False


class Speaker:
    """Text-to-Speech engine utilizing natural, clear neural voices with macOS speech fallback."""

    def __init__(self, voice: str = "en-US-GuyNeural", rate: int = 185, enabled: bool = True):
        self.voice = voice
        self.rate = rate
        self.enabled = enabled
        self._current_process: Optional[subprocess.Popen] = None
        self._lock = threading.Lock()
        self._temp_dir = tempfile.gettempdir()

    def clean_text_for_speech(self, text: str) -> str:
        """Removes markdown syntax, URLs, and code blocks for natural-sounding speech."""
        if not text:
            return ""

        # Remove code blocks ``` ... ```
        cleaned = re.sub(r'```[\s\S]*?```', '', text)
        
        # Remove inline code `code`
        cleaned = re.sub(r'`([^`]+)`', r'\1', cleaned)
        
        # Remove Markdown links [text](url) -> text
        cleaned = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', cleaned)
        
        # Remove markdown symbols (*, _, #, >, -, etc.)
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

    def _speak_neural(self, text: str, wait: bool) -> bool:
        """Synthesizes and plays natural neural speech via edge-tts."""
        if not HAS_EDGE_TTS:
            return False

        temp_audio_file = os.path.join(self._temp_dir, "tars_speech.mp3")

        async def _synth():
            # Use natural neural voice (Guy is clean, natural, simple, and friendly)
            neural_voice = self.voice if "Neural" in self.voice else "en-US-GuyNeural"
            communicate = edge_tts.Communicate(text, neural_voice)
            await communicate.save(temp_audio_file)

        try:
            asyncio.run(_synth())
            if os.path.exists(temp_audio_file) and os.path.getsize(temp_audio_file) > 0:
                if platform.system() == "Darwin":
                    cmd = ["afplay", temp_audio_file]
                    if wait:
                        subprocess.run(cmd, check=False)
                    else:
                        with self._lock:
                            self._current_process = subprocess.Popen(cmd)
                    return True
        except Exception:
            pass

        return False

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

        self.stop()

        # 1. Try crystal-clear natural Neural Voice first
        success = self._speak_neural(speech_text, wait=wait)
        if success:
            return

        # 2. Fallback to clean, simple macOS native voice (Samantha)
        if platform.system() == "Darwin":
            try:
                fallback_voice = "Samantha" if ("Neural" in self.voice or self.voice == "Daniel") else self.voice
                cmd = ["say", "-v", fallback_voice, "-r", str(self.rate), speech_text]
                if wait:
                    subprocess.run(cmd, check=False)
                else:
                    with self._lock:
                        self._current_process = subprocess.Popen(cmd)
            except Exception as e:
                print(f" [Voice Warning] TTS Error: {e}")

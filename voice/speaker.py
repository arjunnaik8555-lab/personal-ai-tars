import asyncio
import os
import platform
import re
import subprocess
import tempfile
import threading
import time
from typing import Optional, Callable

try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False


class Speaker:
    """Text-to-Speech engine with real-time sentence streaming and instant interruption (barge-in)."""

    def __init__(self, voice: str = "en-US-GuyNeural", rate: int = 185, enabled: bool = True):
        self.voice = voice
        self.rate = rate
        self.enabled = enabled
        self._current_process: Optional[subprocess.Popen] = None
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._is_speaking = False
        self._temp_dir = tempfile.gettempdir()

    @property
    def is_speaking(self) -> bool:
        return self._is_speaking

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
        # Remove markdown symbols
        cleaned = re.sub(r'[*_~#>-]', ' ', cleaned)
        # Collapse multiple spaces
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    def split_into_sentences(self, text: str) -> list[str]:
        """Splits long text into manageable sentences for fast, interruptible playback."""
        if not text:
            return []
        # Split by sentence end punctuation or newlines
        raw_chunks = re.split(r'(?<=[.!?\n])\s+', text)
        sentences = [c.strip() for c in raw_chunks if c.strip()]
        return sentences

    def stop(self):
        """Immediately interrupts and halts any currently playing or scheduled speech."""
        self._stop_event.set()
        with self._lock:
            if self._current_process and self._current_process.poll() is None:
                try:
                    self._current_process.terminate()
                    self._current_process.kill()
                except Exception:
                    pass
                self._current_process = None

            # Force kill any active afplay on macOS
            if platform.system() == "Darwin":
                try:
                    subprocess.run(["pkill", "-9", "-f", "tars_sentence_"], capture_output=True, check=False)
                except Exception:
                    pass
        self._is_speaking = False

    def _play_audio_process(self, cmd: list[str]) -> bool:
        """Runs audio command asynchronously while constantly monitoring for stop interrupt."""
        if self._stop_event.is_set():
            return False

        with self._lock:
            try:
                self._current_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                return False

        # Poll process status every 40ms to catch user interruptions instantly
        while self._current_process and self._current_process.poll() is None:
            if self._stop_event.is_set():
                self.stop()
                return False
            time.sleep(0.04)

        return True

    def _speak_sentence_neural(self, sentence: str, file_idx: int) -> bool:
        """Synthesizes and plays a single sentence using edge-tts."""
        if not HAS_EDGE_TTS or self._stop_event.is_set():
            return False

        temp_audio = os.path.join(self._temp_dir, f"tars_sentence_{file_idx}.mp3")

        async def _synth():
            neural_voice = self.voice if "Neural" in self.voice else "en-US-GuyNeural"
            communicate = edge_tts.Communicate(sentence, neural_voice)
            await communicate.save(temp_audio)

        try:
            asyncio.run(_synth())
            if os.path.exists(temp_audio) and os.path.getsize(temp_audio) > 0:
                if platform.system() == "Darwin":
                    return self._play_audio_process(["afplay", temp_audio])
        except Exception:
            pass

        return False

    def _speak_sentence_fallback(self, sentence: str) -> bool:
        """Fallback to native macOS say."""
        if platform.system() == "Darwin" and not self._stop_event.is_set():
            fallback_voice = "Samantha" if ("Neural" in self.voice or self.voice == "Daniel") else self.voice
            cmd = ["say", "-v", fallback_voice, "-r", str(self.rate), sentence]
            return self._play_audio_process(cmd)
        return False

    def speak(self, text: str, on_sentence: Optional[Callable[[str], None]] = None):
        """Speaks text sentence-by-sentence. Can be instantly stopped at any time by calling stop()."""
        if not self.enabled:
            return

        speech_text = self.clean_text_for_speech(text)
        if not speech_text:
            return

        self._stop_event.clear()
        self._is_speaking = True

        sentences = self.split_into_sentences(speech_text)

        try:
            for idx, sentence in enumerate(sentences):
                if self._stop_event.is_set():
                    break

                if on_sentence:
                    on_sentence(sentence)

                # Try Neural speech, then fallback
                success = self._speak_sentence_neural(sentence, idx % 5)
                if not success and not self._stop_event.is_set():
                    self._speak_sentence_fallback(sentence)

        finally:
            self._is_speaking = False

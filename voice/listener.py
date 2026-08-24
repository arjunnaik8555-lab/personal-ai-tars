import speech_recognition as sr
from typing import Optional


class Listener:
    """Speech-to-Text engine capturing and transcribing microphone audio with intelligent pause handling."""

    def __init__(self, pause_threshold: float = 1.8, language: str = "en-IN", energy_threshold: int = 300):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.dynamic_energy_threshold = True
        
        # Generous pause threshold so natural pauses (1-2 seconds) mid-sentence are not cut off
        self.recognizer.pause_threshold = pause_threshold
        self.recognizer.non_speaking_duration = 0.8
        self.recognizer.phrase_threshold = 0.3
        self.language = language
        self._calibrated = False

    def calibrate_microphone(self, source):
        """Quickly calibrates microphone to background room noise once."""
        if not self._calibrated:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
            self._calibrated = True

    def listen(self, timeout: int = 8, phrase_time_limit: int = 20) -> Optional[str]:
        """Listens from the microphone and returns recognized text.
        
        Args:
            timeout: Max seconds to wait for user to begin speaking.
            phrase_time_limit: Max seconds for a single speech sentence.
            
        Returns:
            Transcribed string or None if silence/error.
        """
        try:
            with sr.Microphone() as source:
                print(" 🎙️  [TARS Listening...] (Speak naturally, pauses are supported)")
                self.calibrate_microphone(source)
                
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
            print(" ⏳ [Transcribing audio...]")
            
            # Try configured language first (e.g. en-IN), fallback to en-US
            try:
                text = self.recognizer.recognize_google(audio, language=self.language)
            except Exception:
                text = self.recognizer.recognize_google(audio, language="en-US")
                
            return text.strip() if text else None

        except sr.WaitTimeoutError:
            print(" ⏱️  [Listening timed out — no speech detected]")
            return None
        except sr.UnknownValueError:
            print(" 🤔 [Could not understand audio — please try again]")
            return None
        except sr.RequestError as e:
            print(f" ❌ [Speech Recognition network error: {e}]")
            return None
        except Exception as e:
            print(f" ❌ [Microphone error: {e}]")
            return None

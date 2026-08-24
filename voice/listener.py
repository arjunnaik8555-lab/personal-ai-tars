import speech_recognition as sr
from typing import Optional


class Listener:
    """Speech-to-Text engine capturing audio from the microphone."""

    def __init__(self, energy_threshold: int = 300):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

    def listen(self, timeout: int = 7, phrase_time_limit: int = 15) -> Optional[str]:
        """Listens from the microphone and returns recognized text.
        
        Args:
            timeout: Max seconds to wait for user to begin speaking.
            phrase_time_limit: Max seconds for a single speech phrase.
            
        Returns:
            Transcribed string or None if silence/error.
        """
        try:
            with sr.Microphone() as source:
                print(" 🎙️  [TARS Listening...] (Speak now)")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
            print(" ⏳ [Processing audio...]")
            text = self.recognizer.recognize_google(audio)
            return text.strip()

        except sr.WaitTimeoutError:
            print(" ⏱️  [Listening timed out — no speech detected]")
            return None
        except sr.UnknownValueError:
            print(" 🤔 [Could not understand audio]")
            return None
        except sr.RequestError as e:
            print(f" ❌ [Speech Recognition service error: {e}]")
            return None
        except Exception as e:
            print(f" ❌ [Microphone error: {e}]")
            return None

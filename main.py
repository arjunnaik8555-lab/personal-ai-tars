import sys
import threading
from agent.agent import TarsAgent
from config.settings import (
    GEMINI_MODEL,
    VOICE_ENABLED,
    VOICE_NAME,
    VOICE_RATE,
    VOICE_PAUSE_SECONDS,
    SPEECH_LANGUAGE,
)
from voice import Speaker, Listener


def main():
    print("=" * 65)
    print("🤖 TARS System Online [Real-Time Voice & Interruptible Speech]")
    print(f"🧠 Model: {GEMINI_MODEL}")
    print(f"🔊 Voice: {'Enabled' if VOICE_ENABLED else 'Disabled'} ({VOICE_NAME})")
    print(f"🎙️  STT Language: {SPEECH_LANGUAGE} | Pause Tolerance: {VOICE_PAUSE_SECONDS}s")
    print("🎙️  Commands:")
    print("   • Type 'v' or 'voice'  ➔ Switch to Voice Mode (hands-free speaking)")
    print("   • Type 't' or 'text'   ➔ Switch to Text Mode (keyboard typing)")
    print("   • Press Ctrl+C         ➔ Instantly interrupt TARS while it is talking")
    print("   • Type 'mute'/'unmute' ➔ Toggle spoken audio on/off")
    print("   • Type 'exit'          ➔ Power down TARS")
    print("=" * 65)

    try:
        tars = TarsAgent()
    except Exception as e:
        print(f"\n❌ Initialization Error: {e}")
        sys.exit(1)

    speaker = Speaker(voice=VOICE_NAME, rate=VOICE_RATE, enabled=VOICE_ENABLED)
    listener = Listener(pause_threshold=VOICE_PAUSE_SECONDS, language=SPEECH_LANGUAGE)
    voice_mode = False

    # Optional boot-up greeting
    try:
        speaker.speak("TARS systems online and operational.")
    except Exception:
        pass

    while True:
        try:
            if voice_mode:
                print("\n" + "-" * 40)
                print("🎤 [Voice Mode Active] (Press Ctrl+C to return to Text Mode)")
                spoken_input = listener.listen(timeout=8, phrase_time_limit=18)

                if spoken_input is None:
                    continue

                user_message = spoken_input
                print(f"You (Spoken): {user_message}")

                if user_message.lower() in ["exit", "quit", "bye", "goodbye", "shut down"]:
                    print("\nTARS: Shutting down systems. Goodbye.")
                    speaker.speak("Shutting down systems. Goodbye.")
                    break
                elif user_message.lower() in ["text mode", "switch to text"]:
                    print("\n🔁 Switching to Text Mode.")
                    speaker.speak("Switching to text mode.")
                    voice_mode = False
                    continue

            else:
                user_message = input("\nYou: ").strip()

                if not user_message:
                    continue

                lower_msg = user_message.lower()

                if lower_msg in ["exit", "quit", "bye"]:
                    print("\nTARS: Shutting down systems. Goodbye.")
                    speaker.speak("Shutting down systems. Goodbye.")
                    break

                if lower_msg in ["v", "voice", "voice mode"]:
                    voice_mode = True
                    print("\n🎙️ Switched to Voice Mode. Start speaking!")
                    speaker.speak("Voice mode activated. What can I do for you?")
                    continue

                if lower_msg in ["t", "text", "text mode"]:
                    voice_mode = False
                    print("\n⌨️ In Text Mode.")
                    continue

                if lower_msg == "mute":
                    speaker.enabled = False
                    print("🔇 Audio voice muted.")
                    continue
                elif lower_msg == "unmute":
                    speaker.enabled = True
                    print("🔊 Audio voice unmuted.")
                    continue

            # Generate response from Gemini with tools
            response = tars.chat(user_message)
            print(f"\nTARS: {response}\n")

            # Speak response with instant Ctrl+C interruption support
            try:
                speaker.speak(response)
            except KeyboardInterrupt:
                speaker.stop()
                print("\n🛑 [Interrupted TARS speech]")

        except KeyboardInterrupt:
            speaker.stop()
            if voice_mode:
                print("\n\n🔁 Exiting Voice Mode, returning to Text Mode.")
                voice_mode = False
                continue
            else:
                print("\n\nTARS: Emergency override received. Powering down.")
                break
        except Exception as e:
            print(f"\nTARS Error: {str(e)}")


if __name__ == "__main__":
    main()

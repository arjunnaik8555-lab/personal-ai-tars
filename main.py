import sys
from agent.agent import TarsAgent
from config.settings import (
    GEMINI_MODEL,
    VOICE_ENABLED,
    VOICE_NAME,
    VOICE_RATE,
    VOICE_PAUSE_SECONDS,
    SPEECH_LANGUAGE,
)
from memory.database import global_db
from voice import Speaker, Listener


def print_banner():
    print("=" * 68)
    print("🤖 TARS FULL SYSTEM ONLINE [All Milestones Active]")
    print(f"🧠 Primary Model: {GEMINI_MODEL}")
    print(f"🔊 Voice TTS: {'Enabled' if VOICE_ENABLED else 'Disabled'} ({VOICE_NAME})")
    print(f"🎙️  STT Language: {SPEECH_LANGUAGE} | Pause Tolerance: {VOICE_PAUSE_SECONDS}s")
    print("-" * 68)
    print("🛠️  Capabilities:")
    print("   • System & OS      ➔ Apps, Time, Battery, Shell commands")
    print("   • Web & Chrome     ➔ Live Google/DDG Search, Chrome, Weather")
    print("   • Workspace & Files➔ Search, Read, Write & Edit workspace files")
    print("   • Memory (SQLite)  ➔ Remembers user facts & chat history")
    print("   • Vision (Screen)  ➔ Screen capture & visual analysis")
    print("   • Messaging        ➔ WhatsApp messaging")
    print("   • Personality      ➔ Adjustable Humor & Honesty dials")
    print("-" * 68)
    print("💡 Commands:")
    print("   • 'v' or 'voice'    ➔ Switch to Hands-Free Voice Mode")
    print("   • 't' or 'text'     ➔ Switch to Text Mode")
    print("   • 'screen'          ➔ Analyze current desktop screen visually")
    print("   • 'briefing'        ➔ Generate full Daily Morning Briefing")
    print("   • 'memory'          ➔ View remembered user facts")
    print("   • 'mute'/'unmute'   ➔ Toggle audio voice")
    print("   • 'exit'            ➔ Shut down TARS")
    print("=" * 68)


def main():
    print_banner()

    try:
        tars = TarsAgent()
    except Exception as e:
        print(f"\n❌ Initialization Error: {e}")
        sys.exit(1)

    speaker = Speaker(voice=VOICE_NAME, rate=VOICE_RATE, enabled=VOICE_ENABLED)
    listener = Listener(pause_threshold=VOICE_PAUSE_SECONDS, language=SPEECH_LANGUAGE)
    voice_mode = False

    # Greeting
    try:
        speaker.speak("TARS fully operational. Ready for orders.")
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

                if lower_msg in ["screen", "vision", "see screen"]:
                    user_message = "Analyze my current desktop screen and tell me what is visible."

                if lower_msg == "briefing":
                    user_message = "Give me my full daily briefing."

                if lower_msg in ["memory", "facts"]:
                    facts = global_db.get_all_facts()
                    print("\n🧠 [Remembered User Facts]:")
                    if facts:
                        for f in facts:
                            print(f" • {f['key']}: {f['fact']}")
                    else:
                        print(" No facts stored yet. Tell TARS 'Remember that my name is...' to save facts.")
                    continue

                if lower_msg == "mute":
                    speaker.enabled = False
                    print("🔇 Audio voice muted.")
                    continue
                elif lower_msg == "unmute":
                    speaker.enabled = True
                    print("🔊 Audio voice unmuted.")
                    continue

            # Process prompt with Gemini and execute tools
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

import sys
from agent.agent import TarsAgent
from config.settings import GEMINI_MODEL


def main():
    print("=" * 60)
    print("🤖 TARS System Online [Phase 1: Tool-Calling Engine]")
    print(f"🧠 Model: {GEMINI_MODEL}")
    print("🛠️  Capabilities: Time check, System/Battery status, App launcher")
    print("💡 Type 'exit', 'quit', or 'bye' to power down.")
    print("=" * 60)

    try:
        tars = TarsAgent()
    except Exception as e:
        print(f"\n❌ Initialization Error: {e}")
        sys.exit(1)

    while True:
        try:
            user_message = input("\nYou: ").strip()

            if not user_message:
                continue

            if user_message.lower() in ["exit", "quit", "bye"]:
                print("\nTARS: Shutting down systems. Goodbye.")
                break

            response = tars.chat(user_message)
            print(f"\nTARS: {response}")

        except KeyboardInterrupt:
            print("\n\nTARS: Emergency override received. Powering down.")
            break
        except Exception as e:
            print(f"\nTARS Error: {str(e)}")


if __name__ == "__main__":
    main()

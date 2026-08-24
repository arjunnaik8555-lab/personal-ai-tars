import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not set. Please create a .env file and add your GEMINI_API_KEY. "
        "Refer to .env.example for guidance."
    )

# Voice configuration (macOS speech)
VOICE_ENABLED = os.getenv("VOICE_ENABLED", "true").lower() in ("true", "1", "yes")
VOICE_NAME = os.getenv("VOICE_NAME", "Daniel")
VOICE_RATE = int(os.getenv("VOICE_RATE", "185"))

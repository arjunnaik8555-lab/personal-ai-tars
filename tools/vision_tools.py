import os
import subprocess
import tempfile
from PIL import ImageGrab
from google import genai
from google.genai import types

from config.settings import GEMINI_API_KEY, GEMINI_MODEL


def capture_screenshot(save_path: str = "/tmp/tars_screenshot.png") -> str:
    """Captures a screenshot of the user's current Mac screen and saves it."""
    print("\n  👁️  [TARS Action] Capturing screen image...")
    try:
        if os.name == "posix":
            res = subprocess.run(["screencapture", "-x", save_path], capture_output=True, check=False)
            if res.returncode == 0 and os.path.exists(save_path):
                return save_path

        # Fallback to PIL ImageGrab
        img = ImageGrab.grab()
        img.save(save_path)
        return save_path
    except Exception as e:
        print(f"Failed to capture screenshot: {e}")
        return ""


def analyze_screen(question: str = "Describe what is currently visible on the screen, identify open applications, code, errors, or key details.") -> str:
    """Takes a screenshot of the user's active screen and uses Gemini Vision to see, analyze, and explain what is on the screen.
    
    Args:
        question: Specific question about what's on screen (e.g., 'What error is in my code?', 'Summarize this webpage', 'Where is the submit button?').
    """
    print(f"\n  👁️  [TARS Action] Analyzing screen vision for query: '{question}'...")
    screenshot_path = os.path.join(tempfile.gettempdir(), "tars_vision_screen.png")
    captured = capture_screenshot(screenshot_path)

    if not captured or not os.path.exists(screenshot_path):
        return "Failed to capture screen image."

    try:
        with open(screenshot_path, "rb") as f:
            image_bytes = f.read()

        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = (
            f"User Question about Screen: {question}\n\n"
            "You are TARS, a personal AI robot assistant. Analyze this screenshot of the user's desktop computer. "
            "Provide a concise, practical, and helpful answer to the user's question."
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[
                prompt,
                types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
            ]
        )

        return response.text if response.text else "Screen analyzed, no text returned."

    except Exception as e:
        return f"Screen vision analysis failed: {str(e)}"

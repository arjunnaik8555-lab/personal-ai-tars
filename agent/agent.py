import time
from google import genai
from google.genai import types

from config.settings import GEMINI_API_KEY, GEMINI_MODEL
from tools import ALL_TOOLS


FALLBACK_MODELS = [GEMINI_MODEL, "gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-flash-lite-latest"]


class TarsAgent:
    """TARS Agent capable of reasoning, conversation, internet browsing, and executing local tools."""

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.active_model = GEMINI_MODEL
        
        self.system_instruction = (
            "You are TARS, a personal AI robot assistant inspired by Interstellar. "
            "You are intelligent, practical, highly capable, concise, and have a subtle wit. "
            "You have direct access to tools to interact with the user's computer and the internet:\n"
            "1. Web Search & Browsing: search_web for real-time info, facts, news, documentation; "
            "fetch_webpage_content to inspect specific websites; open_in_browser to launch URLs or Google searches in Google Chrome.\n"
            "2. Weather: get_weather for live global temperature and weather forecasts.\n"
            "3. System Tools: get_current_time, get_system_status, open_application.\n"
            "When the user asks any question requiring up-to-date information, facts, live data, or web actions, "
            "use your tools proactively to find accurate answers."
        )

        self._init_chat_session(self.active_model)

    def _init_chat_session(self, model_name: str):
        """Initializes a multi-turn chat session with tools enabled."""
        config = types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            tools=ALL_TOOLS,
            temperature=0.7,
        )
        self.chat_session = self.client.chats.create(
            model=model_name,
            config=config,
        )
        self.active_model = model_name

    def chat(self, user_message: str) -> str:
        """Sends a user message to Gemini, auto-executes tools if needed, with automatic model fallback on quota limits."""
        # Try active model first, then fallback models if rate-limited (429)
        tried_models = set()
        
        for model in [self.active_model] + FALLBACK_MODELS:
            if model in tried_models:
                continue
            tried_models.add(model)

            try:
                if self.active_model != model:
                    self._init_chat_session(model)

                response = self.chat_session.send_message(user_message)
                return response.text if response.text else "Done."

            except Exception as e:
                err_str = str(e)
                # If quota exceeded (429) or unavailable (503), try next fallback model
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "503" in err_str:
                    print(f" ⚠️ [Model {model} busy or rate-limited. Switching to fallback...]")
                    time.sleep(1)
                    continue
                else:
                    return f"Error communicating with TARS core: {err_str}"

        return "TARS core systems are temporarily rate-limited. Please wait a moment and try again."

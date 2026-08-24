from google import genai
from google.genai import types

from config.settings import GEMINI_API_KEY, GEMINI_MODEL
from tools import ALL_TOOLS


class TarsAgent:
    """TARS Agent capable of reasoning, conversation, internet browsing, and executing local tools."""

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        
        self.system_instruction = (
            "You are TARS, a personal AI robot assistant inspired by Interstellar. "
            "You are intelligent, practical, highly capable, concise, and have a subtle wit. "
            "You have direct access to tools to interact with the user's computer and the internet:\n"
            "1. Web Search & Browsing: search_web for real-time information, news, questions, documentation; "
            "fetch_webpage_content to read specific webpages/articles; open_in_browser to open URLs or searches in Google Chrome.\n"
            "2. Weather: get_weather for live weather in any location.\n"
            "3. System Tools: get_current_time, get_system_status, open_application.\n"
            "When the user asks any question requiring up-to-date information, facts, live data, or web actions, "
            "use your tools proactively to find accurate answers."
        )

        config = types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            tools=ALL_TOOLS,
            temperature=0.7,
        )

        # Create multi-turn chat session with tools enabled
        self.chat_session = self.client.chats.create(
            model=GEMINI_MODEL,
            config=config,
        )

    def chat(self, user_message: str) -> str:
        """Sends a user message to Gemini, auto-executes tools if needed, and returns the response."""
        try:
            response = self.chat_session.send_message(user_message)
            return response.text if response.text else "Done."
        except Exception as e:
            return f"Error communicating with TARS core: {str(e)}"

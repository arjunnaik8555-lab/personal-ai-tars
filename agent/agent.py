from google import genai
from google.genai import types

from config.settings import GEMINI_API_KEY, GEMINI_MODEL
from tools import ALL_TOOLS


class TarsAgent:
    """TARS Agent capable of reasoning, conversation, and executing local system tools."""

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        
        self.system_instruction = (
            "You are TARS, a personal AI robot assistant inspired by Interstellar. "
            "You are intelligent, practical, highly capable, concise, and have a subtle wit. "
            "You have direct access to tools to interact with the user's computer "
            "(e.g., getting current time, checking system and battery status, launching applications). "
            "When the user asks for actions or real-time info, use your tools proactively."
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

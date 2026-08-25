import time
import uuid
from google import genai
from google.genai import types

from config.settings import GEMINI_API_KEY, GEMINI_MODEL
from memory.database import global_db
from agent.personality import global_personality
from tools import ALL_TOOLS


FALLBACK_MODELS = [GEMINI_MODEL, "gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-flash-lite-latest"]


class TarsAgent:
    """Complete TARS Agent with reasoning, tool calling, persistent memory, vision, and dynamic personality."""

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.active_model = GEMINI_MODEL
        self.session_id = str(uuid.uuid4())[:8]

        self._init_chat_session(self.active_model)

    def _build_system_instruction(self) -> str:
        """Constructs system prompt combining persona, long-term memory facts, and tool guidelines."""
        facts = global_db.get_all_facts()
        fact_str = ""
        if facts:
            fact_str = "\nREMEMBERED USER FACTS & PREFERENCES:\n" + "\n".join([f"- {f['key']}: {f['fact']}" for f in facts])

        personality_str = global_personality.get_system_prompt_segment()

        return (
            "You are TARS, an autonomous personal AI robot assistant inspired by Interstellar.\n\n"
            f"{personality_str}\n"
            f"{fact_str}\n\n"
            "VOICE & SPEECH UNDERSTANDING:\n"
            "- The user talks to you via voice microphone and text. Voice transcriptions may have slight phonetic slips, "
            "missing prepositions, accents, or typos. Intelligently deduce the intended meaning.\n\n"
            "TOOLS & CAPABILITIES:\n"
            "1. File System & Terminal: search_files, read_file_content, write_file_content, list_directory, run_terminal_command.\n"
            "2. Persistent Memory: save_user_fact to store new preferences/details, recall_user_facts, search_past_conversations.\n"
            "3. Multimodal Vision: analyze_screen to capture and see what's on the user's screen.\n"
            "4. Web Search & Browsing: search_web, fetch_webpage_content, open_in_browser, get_weather.\n"
            "5. Messaging & Control: send_whatsapp_message, get_current_time, get_system_status, open_application.\n"
            "6. Personality & Schedulers: set_personality_parameters, set_reminder, get_daily_briefing.\n\n"
            "Execute tools proactively to fulfill user requests."
        )

    def _init_chat_session(self, model_name: str):
        """Initializes a multi-turn chat session with tools enabled."""
        system_instruction = self._build_system_instruction()
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=ALL_TOOLS,
            temperature=0.7,
        )
        self.chat_session = self.client.chats.create(
            model=model_name,
            config=config,
        )
        self.active_model = model_name

    def chat(self, user_message: str) -> str:
        """Sends a user message to Gemini, auto-executes tools, logs to SQLite memory, and returns the response."""
        # Log user input
        global_db.log_message(self.session_id, "user", user_message)

        tried_models = set()
        for model in [self.active_model] + FALLBACK_MODELS:
            if model in tried_models:
                continue
            tried_models.add(model)

            try:
                if self.active_model != model:
                    self._init_chat_session(model)

                response = self.chat_session.send_message(user_message)
                answer = response.text if response.text else "Done."
                
                # Log agent response to SQLite
                global_db.log_message(self.session_id, "assistant", answer)
                return answer

            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "503" in err_str:
                    print(f" ⚠️ [Model {model} busy or rate-limited. Switching to fallback...]")
                    time.sleep(1)
                    continue
                else:
                    return f"Error communicating with TARS core: {err_str}"

        return "TARS core systems are temporarily rate-limited. Please wait a moment and try again."

# 🤖 Personal AI TARS

A modular, autonomous AI assistant inspired by TARS from *Interstellar*, built with Google Gemini and Python.

---

## 🚀 Capabilities & Milestones

### Milestone 1: Tool-Calling Engine & System Control
- **Native Tool Calling**: Gemini autonomously chooses when to execute Python tools vs when to converse.
- **System Tools**:
  - `get_current_time()`: Local timestamp, date, and timezone.
  - `get_system_status()`: macOS battery percentage, charging state, OS and hardware specs.
  - `open_application(app_name)`: Launches macOS desktop applications (e.g. Spotify, Notes, Calculator, Terminal).
  - `run_terminal_command(command)`: Executes shell commands on your Mac.

### Milestone 2: Voice & Hands-Free Interaction
- **Speech-to-Text (STT)**: Microphone speech recognition with dynamic noise calibration and generous pause tolerance (`VOICE_PAUSE_SECONDS`).
- **Natural Neural TTS**: Crystal-clear neural voice synthesis (`edge-tts` with `en-US-GuyNeural` / fallback to macOS `Samantha`/`Rishi`).
- **Instant Interruption (Barge-In)**: Press `Ctrl+C` or speak to cut off speech playback within milliseconds.
- **Interactive Modes**: Text Mode (`t`) or Hands-Free Voice Mode (`v`).

### Milestone 3: Web Search, Chrome & Live Intelligence
- **Live Web Search (`search_web`)**: Real-time web search for any question, current news, sports scores, tutorials, and research.
- **Google Chrome Integration (`open_in_browser`)**: Opens URLs and Google searches directly in Google Chrome.
- **Webpage Reader (`fetch_webpage_content`)**: Scrapes and analyzes articles, documentation, or links.
- **Live Weather (`get_weather`)**: Real-time global weather report.
- **WhatsApp Integration (`send_whatsapp_message`)**: Opens WhatsApp Desktop/Web chats with pre-populated messages.

### Milestone 4: Workspace & File System Automation
- **`search_files(query, search_path)`**: Finds files, documents, or code anywhere in your workspace or filesystem.
- **`read_file_content(file_path)`**: Reads code, markdown, notes, or data files.
- **`write_file_content(file_path, content)`**: Creates or edits files.
- **`list_directory(directory_path)`**: Lists folders and file sizes.

### Milestone 5: Persistent Long-Term Memory (SQLite)
- **SQLite Database (`data/tars_memory.db`)**: Stores facts, user preferences, and conversation logs permanently across restarts.
- **`save_user_fact(key, fact)`**: Saves key facts about you (name, projects, preferences, habits).
- **`recall_user_facts(query)`**: Recalls stored facts on command.
- **`search_past_conversations(query)`**: Searches past chat sessions.

### Milestone 6: Multimodal Vision & Screen Perception
- **`analyze_screen(question)`**: Takes a screenshot of your active Mac screen and uses Gemini Vision to explain code, UI, errors, or diagrams on screen.

### Milestone 7: Interstellar Personality & Proactive Schedulers
- **`set_personality_parameters(humor, honesty)`**: Dynamically adjusts Humor (0–100%) and Honesty (0–100%) dials.
- **`set_reminder(reminder_text, delay_seconds)`**: Sets background timer alarms that speak and alert you when time is up.
- **`get_daily_briefing(city)`**: Generates a daily morning briefing (time, weather, battery/system status, pending memory facts).

---

## 🛠️ Setup & Running

1. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and add your **GEMINI_API_KEY** from [Google AI Studio](https://aistudio.google.com/).

4. **Launch TARS**:
   ```bash
   python main.py
   ```

---

## 🗺️ Project Roadmap
- [x] **Milestone 1**: Core Tool Calling & System Control
- [x] **Milestone 2**: Voice Interface (Speech-to-Text & Text-to-Speech)
- [x] **Milestone 3**: Web Search, Chrome Integration & Live Intelligence
- [x] **Milestone 4**: File System & Workspace Automation
- [x] **Milestone 5**: Persistent Long-Term Memory (SQLite database)
- [x] **Milestone 6**: Multimodal Screen & Vision Perception
- [x] **Milestone 7**: Personality Tuning (Humor / Honesty) & Autonomous Schedulers

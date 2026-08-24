# 🤖 Personal AI TARS

A modular, autonomous AI assistant inspired by TARS from *Interstellar*, built with Google Gemini and Python.

---

## 🚀 Capabilities

### Milestone 1: Tool-Calling Engine & System Hands
- **Native Tool Calling**: TARS decides when to invoke local Python tools vs when to chat.
- **System Tools**:
  - `get_current_time()`: Local timestamp, date, and timezone.
  - `get_system_status()`: macOS battery percentage, charging state, OS and hardware specs.
  - `open_application(app_name)`: Launches macOS desktop applications (e.g. Spotify, Notes, Calculator, Terminal).

### Milestone 2: Voice & Hands-Free Interaction
- **Speech-to-Text (STT)**: Microphone listening with ambient noise suppression.
- **Text-to-Speech (TTS)**: High-speed, natural speech synthesis powered by macOS speech (configurable voice, e.g. `Daniel`).
- **Interactive Modes**:
  - `[T] Text Mode`: Standard keyboard input with spoken responses.
  - `[V] Voice Mode`: Complete hands-free conversational loop (speak & listen).
  - Quick commands: `voice` / `v`, `text` / `t`, `mute` / `unmute`.

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
- [ ] **Milestone 3**: Web Search & Real-Time Info
- [ ] **Milestone 4**: File System & Workspace Automation
- [ ] **Milestone 5**: Persistent Long-Term Memory (SQLite)
- [ ] **Milestone 6**: Multimodal Screen & Vision Perception
- [ ] **Milestone 7**: Personality Tuning (Humor / Honesty) & Autonomous Schedulers

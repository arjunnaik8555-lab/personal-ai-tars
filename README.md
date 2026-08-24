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
- [ ] **Milestone 2**: Web Search & Real-Time Info
- [ ] **Milestone 3**: File System & Workspace Automation
- [ ] **Milestone 4**: Persistent Memory (SQLite)
- [ ] **Milestone 5**: Voice Interface (Speech-to-Text & TTS)
- [ ] **Milestone 6**: Multimodal Screen & Vision Perception
- [ ] **Milestone 7**: Personality Tuning (Humor / Honesty) & Autonomous Schedulers

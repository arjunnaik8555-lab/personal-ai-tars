import datetime
import os
import sqlite3
from typing import List, Dict, Optional


DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "tars_memory.db")


class MemoryDatabase:
    """Persistent SQLite database manager for TARS conversation history, user facts, and reminders."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Creates necessary tables if they do not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Conversation logs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    role TEXT,
                    content TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # User facts and preferences
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_facts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE,
                    fact TEXT,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Reminders and scheduled tasks
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT,
                    due_time TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    # --- Conversation Logging ---
    def log_message(self, session_id: str, role: str, content: str):
        """Logs a chat turn to the database."""
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO conversations (session_id, role, content) VALUES (?, ?, ?)",
                (session_id, role, content)
            )
            conn.commit()

    def search_conversations(self, query: str, limit: int = 5) -> List[Dict]:
        """Searches past conversations for matching keywords."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT session_id, role, content, timestamp FROM conversations WHERE content LIKE ? ORDER BY id DESC LIMIT ?",
                (f"%{query}%", limit)
            )
            return [dict(row) for row in cursor.fetchall()]

    # --- User Facts & Long-Term Memory ---
    def save_fact(self, key: str, fact: str) -> str:
        """Inserts or updates a personal fact/preference about the user."""
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO user_facts (key, fact, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP) "
                "ON CONFLICT(key) DO UPDATE SET fact=excluded.fact, updated_at=CURRENT_TIMESTAMP",
                (key.strip().lower(), fact.strip())
            )
            conn.commit()
        return f"Stored fact for '{key}': {fact}"

    def get_all_facts(self) -> List[Dict]:
        """Returns all remembered facts."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT key, fact, updated_at FROM user_facts ORDER BY updated_at DESC")
            return [dict(row) for row in cursor.fetchall()]

    def search_facts(self, query: str = "") -> List[Dict]:
        """Finds facts matching a keyword or returns all if empty."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if query:
                cursor.execute(
                    "SELECT key, fact, updated_at FROM user_facts WHERE key LIKE ? OR fact LIKE ? ORDER BY updated_at DESC",
                    (f"%{query}%", f"%{query}%")
                )
            else:
                cursor.execute("SELECT key, fact, updated_at FROM user_facts ORDER BY updated_at DESC")
            return [dict(row) for row in cursor.fetchall()]

    # --- Reminders ---
    def add_reminder(self, task: str, due_time: str) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO reminders (task, due_time) VALUES (?, ?)",
                (task, due_time)
            )
            conn.commit()
            return cursor.lastrowid

    def get_pending_reminders(self) -> List[Dict]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, task, due_time FROM reminders WHERE status = 'pending' ORDER BY id ASC")
            return [dict(row) for row in cursor.fetchall()]

    def complete_reminder(self, reminder_id: int):
        with self._get_connection() as conn:
            conn.execute("UPDATE reminders SET status = 'completed' WHERE id = ?", (reminder_id,))
            conn.commit()


# Singleton instance
global_db = MemoryDatabase()


# --- Memory Tools for Gemini ---

def save_user_fact(key: str, fact: str) -> str:
    """Saves a permanent fact, preference, or detail about the user into long-term memory.
    
    Args:
        key: Category or identifier (e.g., 'user_name', 'favorite_music', 'project_deadline', 'coffee_preference').
        fact: The information to remember (e.g., 'Arjun', 'Loves ambient synthwave', 'Paper submission is on Friday').
    """
    print(f"\n  🧠 [TARS Action] Saving to long-term memory: [{key}] -> {fact}...")
    res = global_db.save_fact(key, fact)
    return res


def recall_user_facts(query: str = "") -> str:
    """Recalls stored facts, preferences, or personal details about the user from long-term memory.
    
    Args:
        query: Optional keyword to filter facts (leave empty to view all known facts).
    """
    print(f"\n  🧠 [TARS Action] Recalling facts from long-term memory (query: '{query}')...")
    facts = global_db.search_facts(query)
    if not facts:
        return "No matching facts found in long-term memory."

    formatted = ["Remembered Facts:"]
    for f in facts:
        formatted.append(f" • **{f['key']}**: {f['fact']}")
    return "\n".join(formatted)


def search_past_conversations(query: str, limit: int = 5) -> str:
    """Searches past conversation logs for specific keywords or topics discussed in earlier sessions.
    
    Args:
        query: Topic or keyword to find in previous chat logs.
        limit: Number of matches to return (default 5).
    """
    print(f"\n  🧠 [TARS Action] Searching past conversations for: '{query}'...")
    results = global_db.search_conversations(query, limit=limit)
    if not results:
        return f"No past conversation found referencing '{query}'."

    formatted = [f"Found {len(results)} past reference(s):"]
    for r in results:
        formatted.append(f"[{r['timestamp']}] {r['role'].capitalize()}: {r['content'][:150]}")
    return "\n".join(formatted)

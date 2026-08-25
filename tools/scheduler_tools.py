import datetime
import threading
import time
from memory.database import global_db
from tools.system_tools import get_current_time, get_system_status
from tools.web_tools import get_weather


def _trigger_reminder_alarm(task: str, delay_seconds: int):
    """Background worker function for reminders."""
    time.sleep(delay_seconds)
    print("\n" + "=" * 50)
    print(f" ⏰ [TARS REMINDER ALARM]: {task}")
    print("=" * 50 + "\n")
    try:
        from voice import Speaker
        Speaker().speak(f"Reminder alarm: {task}")
    except Exception:
        pass


def set_reminder(reminder_text: str, delay_seconds: int = 60) -> str:
    """Schedules a timer reminder that will alert and speak to you after the specified seconds.
    
    Args:
        reminder_text: What you want TARS to remind you about (e.g. 'Take a break', 'Join team meeting').
        delay_seconds: Seconds from now when the reminder should trigger (e.g. 300 for 5 minutes, 3600 for 1 hour).
    """
    print(f"\n  ⏰ [TARS Action] Setting reminder '{reminder_text}' in {delay_seconds} seconds...")
    due_time = (datetime.datetime.now() + datetime.timedelta(seconds=delay_seconds)).strftime("%H:%M:%S")
    global_db.add_reminder(reminder_text, due_time)

    # Spawn non-blocking background timer thread
    t = threading.Thread(target=_trigger_reminder_alarm, args=(reminder_text, delay_seconds), daemon=True)
    t.start()

    return f"Reminder set for '{reminder_text}' (triggers at {due_time}, in {delay_seconds} seconds)."


def get_daily_briefing(city: str = "") -> str:
    """Generates a comprehensive daily briefing including time, weather, system status, and saved memory facts.
    
    Args:
        city: City for weather report (e.g., 'Bangalore', 'Mumbai', 'London').
    """
    print("\n  📋 [TARS Action] Generating daily briefing...")
    time_info = get_current_time()
    weather_info = get_weather(city)
    system_info = get_system_status()
    facts = global_db.get_all_facts()

    briefing = [
        "=== 🤖 TARS DAILY BRIEFING ===",
        f"📅 {time_info}",
        f"\n🌤️ Weather:\n{weather_info}",
        f"\n💻 System Status:\n{system_info}",
    ]

    if facts:
        fact_str = "\n".join([f" • {f['key']}: {f['fact']}" for f in facts[:5]])
        briefing.append(f"\n🧠 Key Memory Facts:\n{fact_str}")

    return "\n".join(briefing)

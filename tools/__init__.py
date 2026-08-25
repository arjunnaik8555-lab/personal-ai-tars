from tools.system_tools import (
    get_current_time,
    get_system_status,
    open_application,
)
from tools.web_tools import (
    search_web,
    open_in_browser,
    fetch_webpage_content,
    get_weather,
)
from tools.whatsapp_tools import (
    send_whatsapp_message,
)
from tools.file_tools import (
    search_files,
    read_file_content,
    write_file_content,
    list_directory,
    run_terminal_command,
)
from memory.database import (
    save_user_fact,
    recall_user_facts,
    search_past_conversations,
)
from tools.vision_tools import (
    analyze_screen,
)
from agent.personality import (
    set_personality_parameters,
)
from tools.scheduler_tools import (
    set_reminder,
    get_daily_briefing,
)

# Comprehensive Tool Suite provided to TARS
ALL_TOOLS = [
    # System & Control
    get_current_time,
    get_system_status,
    open_application,
    run_terminal_command,
    
    # Web & Intelligence
    search_web,
    open_in_browser,
    fetch_webpage_content,
    get_weather,
    
    # Communication
    send_whatsapp_message,
    
    # File System & Workspace
    search_files,
    read_file_content,
    write_file_content,
    list_directory,
    
    # Persistent Memory
    save_user_fact,
    recall_user_facts,
    search_past_conversations,
    
    # Vision & Multimodal
    analyze_screen,
    
    # Personality & Scheduler
    set_personality_parameters,
    set_reminder,
    get_daily_briefing,
]

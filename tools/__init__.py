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

# Complete list of callable tools provided to Gemini
ALL_TOOLS = [
    get_current_time,
    get_system_status,
    open_application,
    search_web,
    open_in_browser,
    fetch_webpage_content,
    get_weather,
]

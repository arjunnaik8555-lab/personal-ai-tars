import datetime
import os
import platform
import subprocess


def get_current_time() -> str:
    """Returns the current date, time, day of the week, and timezone on the local machine."""
    print("\n  ⚙️ [TARS Action] Fetching system time...")
    now = datetime.datetime.now().astimezone()
    return now.strftime("Current Date and Time: %A, %B %d, %Y at %I:%M:%S %p (%Z)")


def get_system_status() -> str:
    """Returns system status including OS platform, battery percentage, charging state, and hardware details."""
    print("\n  ⚙️ [TARS Action] Checking system status and battery...")
    info = []
    info.append(f"Operating System: {platform.system()} {platform.release()} ({platform.machine()})")
    
    # macOS battery check
    if platform.system() == "Darwin":
        try:
            battery_output = subprocess.check_output(["pmset", "-g", "batt"], stderr=subprocess.STDOUT, text=True)
            info.append(f"Battery Details:\n{battery_output.strip()}")
        except Exception as e:
            info.append(f"Battery Status: Could not retrieve ({str(e)})")
    
    return "\n".join(info)


def open_application(app_name: str) -> str:
    """Opens an application on the user's computer.
    
    Args:
        app_name: The name of the application to open (e.g. 'Spotify', 'Safari', 'Calculator', 'Notes', 'Visual Studio Code', 'Terminal').
    """
    print(f"\n  ⚙️ [TARS Action] Launching application: {app_name}...")
    if platform.system() != "Darwin":
        return f"open_application is currently configured for macOS. Current OS: {platform.system()}."

    try:
        result = subprocess.run(["open", "-a", app_name], capture_output=True, text=True, check=False)
        if result.returncode == 0:
            return f"Successfully opened application '{app_name}'."
        else:
            err = result.stderr.strip() or "Application not found or unable to launch."
            return f"Could not open application '{app_name}'. Details: {err}"
    except Exception as e:
        return f"Failed to launch '{app_name}': {str(e)}"

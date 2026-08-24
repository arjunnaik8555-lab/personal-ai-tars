import re
import subprocess
import urllib.parse
import webbrowser


def format_phone_number(phone: str) -> str:
    """Formats phone numbers by removing spaces, dashes, and ensuring proper international code."""
    cleaned = re.sub(r"[^\d+]", "", phone.strip())
    # If 10 digits (common Indian mobile number), prepend +91
    if len(cleaned) == 10 and not cleaned.startswith("+"):
        cleaned = "+91" + cleaned
    elif cleaned.startswith("0") and len(cleaned) == 11:
        cleaned = "+91" + cleaned[1:]
    elif not cleaned.startswith("+"):
        cleaned = "+" + cleaned
    return cleaned


def send_whatsapp_message(phone_number: str, message: str) -> str:
    """Opens a WhatsApp chat with a contact or phone number and pre-populates the message.
    
    Args:
        phone_number: The phone number of the recipient (e.g., '+919876543210', '9876543210', or '+14155552671').
        message: The message text to send to the contact.
    """
    print(f"\n  💬 [TARS Action] Opening WhatsApp for recipient: {phone_number}...")
    try:
        formatted_num = format_phone_number(phone_number)
        encoded_msg = urllib.parse.quote(message)
        
        # WhatsApp Web / Desktop Universal Link
        whatsapp_url = f"https://web.whatsapp.com/send?phone={formatted_num.replace('+', '')}&text={encoded_msg}"
        whatsapp_app_url = f"whatsapp://send?phone={formatted_num}&text={encoded_msg}"

        # 1. Try launching WhatsApp Desktop App first if installed
        try:
            res = subprocess.run(["open", whatsapp_app_url], capture_output=True, text=True, check=False)
            if res.returncode == 0:
                return (
                    f"Successfully opened WhatsApp Desktop chat for {formatted_num} with message:\n"
                    f"\"{message}\"\nPress Enter in WhatsApp to dispatch."
                )
        except Exception:
            pass

        # 2. Fallback to WhatsApp Web in Google Chrome / Default browser
        try:
            res = subprocess.run(["open", "-a", "Google Chrome", whatsapp_url], capture_output=True, text=True, check=False)
            if res.returncode == 0:
                return (
                    f"Opened WhatsApp Web in Google Chrome for {formatted_num} with message:\n"
                    f"\"{message}\"\nPress Enter in WhatsApp Web to send."
                )
        except Exception:
            pass

        # 3. Standard browser fallback
        webbrowser.open(whatsapp_url)
        return (
            f"Opened WhatsApp Web for {formatted_num} with message:\n"
            f"\"{message}\"\nPress Enter to send."
        )

    except Exception as e:
        return f"Failed to open WhatsApp: {str(e)}"

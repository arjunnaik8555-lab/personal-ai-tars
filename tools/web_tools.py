import re
import subprocess
import urllib.parse
import webbrowser
from bs4 import BeautifulSoup
import httpx
from ddgs import DDGS


def search_web(query: str, max_results: int = 5) -> str:
    """Searches the live internet for answers, news, articles, facts, or real-time information.
    
    Args:
        query: The search query string (e.g., 'latest AI news', 'who won the match today', 'Python FastAPI tutorial').
        max_results: Number of top results to return (default 5).
    """
    print(f"\n  🌐 [TARS Action] Searching the web for: '{query}'...")
    try:
        results = list(DDGS().text(query, max_results=max_results))
        if not results:
            return f"No search results found for '{query}'."

        formatted = [f"Search results for '{query}':\n"]
        for idx, item in enumerate(results, 1):
            title = item.get("title", "No Title")
            snippet = item.get("body", "No description")
            link = item.get("href", "")
            formatted.append(f"{idx}. **{title}**\n   {snippet}\n   URL: {link}\n")

        return "\n".join(formatted)
    except Exception as e:
        return f"Web search failed: {str(e)}"


def open_in_browser(target: str) -> str:
    """Opens a website or performs a Google Search directly in Google Chrome (or system browser).
    
    Args:
        target: A URL (e.g. 'https://youtube.com', 'https://github.com') or a search phrase (e.g. 'Interstellar cast', 'Reddit AI').
    """
    print(f"\n  🌐 [TARS Action] Opening in Google Chrome: {target}...")
    target = target.strip()
    
    # If not a valid URL, treat as a Google Search query
    if not (target.startswith("http://") or target.startswith("https://") or target.startswith("www.")):
        encoded_query = urllib.parse.quote(target)
        url = f"https://www.google.com/search?q={encoded_query}"
    elif target.startswith("www."):
        url = f"https://{target}"
    else:
        url = target

    # Try launching with Google Chrome on macOS first
    try:
        res = subprocess.run(["open", "-a", "Google Chrome", url], capture_output=True, text=True, check=False)
        if res.returncode == 0:
            return f"Successfully opened '{url}' in Google Chrome."
    except Exception:
        pass

    # Fallback to default system browser
    try:
        webbrowser.open(url)
        return f"Opened '{url}' in default browser."
    except Exception as e:
        return f"Failed to open browser: {str(e)}"


def fetch_webpage_content(url: str) -> str:
    """Fetches and extracts readable text from a webpage URL to analyze or summarize it.
    
    Args:
        url: The web page URL to read (e.g. 'https://en.wikipedia.org/wiki/Artificial_intelligence').
    """
    print(f"\n  🌐 [TARS Action] Fetching webpage: {url}...")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        with httpx.Client(timeout=10, follow_redirects=True, headers=headers) as client:
            response = client.get(url)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts, styles, navs, headers, footers
        for elem in soup(["script", "style", "nav", "header", "footer", "aside", "noscript"]):
            elem.decompose()

        text = soup.get_text(separator=" ", strip=True)
        # Collapse spaces
        text = re.sub(r"\s+", " ", text).strip()

        # Limit to first 4000 characters to fit context nicely
        if len(text) > 4000:
            text = text[:4000] + "... [Content truncated for length]"

        return f"Content of {url}:\n\n{text}"
    except Exception as e:
        return f"Failed to fetch webpage content: {str(e)}"


def get_weather(city: str = "") -> str:
    """Gets real-time weather, temperature, and conditions for any city or location.
    
    Args:
        city: Name of the city (e.g., 'San Francisco', 'London', 'Bangalore', 'Tokyo', 'New York'). If empty, uses IP location.
    """
    print(f"\n  🌐 [TARS Action] Fetching weather forecast for '{city or 'current location'}'...")
    try:
        city_encoded = urllib.parse.quote(city) if city else ""
        url = f"https://wttr.in/{city_encoded}?format=%l:+%c+%t+(Feels+like+%f),+Humidity:+%h,+Wind:+%w"
        
        headers = {"User-Agent": "curl/7.68.0"}
        with httpx.Client(timeout=8, headers=headers) as client:
            res = client.get(url)
            if res.status_code == 200 and res.text:
                return f"Weather report:\n{res.text.strip()}"
            else:
                return f"Could not retrieve weather for {city}."
    except Exception as e:
        return f"Weather request failed: {str(e)}"

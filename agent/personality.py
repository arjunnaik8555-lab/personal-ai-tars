class PersonalityManager:
    """Manages TARS's humor and honesty settings inspired by Interstellar."""

    def __init__(self, humor: int = 75, honesty: int = 90):
        self.humor = humor
        self.honesty = honesty

    def set_parameters(self, humor: int = None, honesty: int = None) -> str:
        if humor is not None:
            self.humor = max(0, min(100, humor))
        if honesty is not None:
            self.honesty = max(0, min(100, honesty))

        return f"TARS Personality Parameters Updated: Humor = {self.humor}%, Honesty = {self.honesty}%."

    def get_system_prompt_segment(self) -> str:
        return (
            f"PERSONALITY SETTINGS:\n"
            f"- Humor Parameter: {self.humor}%\n"
            f"- Honesty Parameter: {self.honesty}%\n"
            f"Maintain an intelligent, practical, highly capable persona. "
            f"If Humor is high (>60%), include subtle dry wit and light banter. "
            f"If Honesty is high (>80%), be direct, accurate, and cut straight to the point."
        )


global_personality = PersonalityManager()


def set_personality_parameters(humor: int = None, honesty: int = None) -> str:
    """Adjusts TARS's humor and honesty parameters (0% to 100%).
    
    Args:
        humor: Humor level from 0 (dead serious) to 100 (maximum sarcasm/jokes).
        honesty: Honesty level from 0 (polite/tactful) to 100 (unfiltered truth).
    """
    print(f"\n  ⚙️ [TARS Action] Adjusting personality: Humor={humor}%, Honesty={honesty}%...")
    return global_personality.set_parameters(humor=humor, honesty=honesty)

class ConversationMemory:

    def __init__(self):
        self.messages = []

    def add_user_message(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        })

    def add_agent_message(self, message):
        self.messages.append({
            "role": "assistant",
            "content": message
        })

    def get_messages(self):
        return self.messages

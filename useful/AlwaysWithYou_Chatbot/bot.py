class Bot:
    def __init__(self, bot_name, relationship, human_name, common_phrases, speaking_style, important_memories, other_background,
                 last_updated, chat_history):
        self.bot_name = bot_name
        self.relationship = relationship
        self.human_name = human_name
        self.common_phrases = common_phrases
        self.speaking_style = speaking_style
        self.important_memories = important_memories
        self.other_background = other_background
        self.last_updated = last_updated
        self.chat_history = chat_history

    def consolidated_info(self):
        info = f"Character's Nickname: {self.bot_name}\n" \
               f"Your Relationship with the Character: {self.relationship}\n" \
               f"Character's Nickname for You: {self.human_name}\n" \
               f"Common Phrases: {self.common_phrases}\n" \
               f"Speaking Style: {self.speaking_style}\n" \
               f"Important Memories:\n{self.important_memories}\n" \
               f"Other Background:\n{self.other_background}"
        return info

    def save_chat_history(self, messages):
        self.chat_history = messages
        
    def get_chat_history(self):
        return self.chat_history
    
    def get_bot_name(self):
        return self.bot_name
    
    def get_human_name(self):
        return self.human_name
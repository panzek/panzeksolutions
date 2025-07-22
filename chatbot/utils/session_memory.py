from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from typing import List, Dict, Any

class DjangoSessionMessageHistory(BaseChatMessageHistory):

    """
    Creates or retrieves a session-based chat history object
    """
    
    # Initialiser
    def __init__(self, session, key="chat_history"):
        self.session = session
        self.key = key
        if self.key not in session:
            self.session[self.key] = []
    
    @property
    def messages(self) -> List:
        raw_messages = self.session.get(self.key, []) # key is the chat_history

        messages = []

        for msg in raw_messages:
            if msg["type"] == "human":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["type"] == "ai":
                messages.append(AIMessage(content=msg["content"]))
        return messages


    def add_message(self, message: BaseMessage) -> None:
        """
        Generic method that adds either a human or ai message, depending on the message type
        """

        if message.type == "human":
            self.add_user_message(message.content)
        elif message.type == "ai":
            self.add_ai_message(message.content)
        else:
            raise ValueError(f"Unsupported message type: {message.type}")
    
    # Adding human message to the session
    def add_user_message(self, message: str) -> None:
        self._append({"type":"human", "content":message})

    # Adding AI message to the session
    def add_ai_message(self, message:str) -> None:
        self._append({"type":"ai", "content":message})

    # Remove all messages from the seesion
    def clear(self) -> None:
        self.session[self.key] = []

    def _append(self, message: Dict[str, Any]) -> None:
        history = self.session.get(self.key, [])
        history.append(message)
        self.session[self.key] = history
        self.session.modified = True
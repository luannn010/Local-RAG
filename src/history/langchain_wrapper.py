from src.history.db import ChatHistory
from langchain_core.messages import HumanMessage, AIMessage
import uuid

class LangChainHistory:
    def __init__(self, session_id: str, manager):
        self.session_id = session_id
        self.manager = manager

    def add_user_message(self, message: str):
        self.manager.save_message(self.session_id, "user", message)

    def add_ai_message(self, message: str):
        self.manager.save_message(self.session_id, "assistant", message)

    def get_messages(self):
        rows = ChatHistory.select().where(ChatHistory.session_id == uuid.UUID(self.session_id)).order_by(ChatHistory.timestamp)
        return [
            HumanMessage(content=row.message) if row.role == "user" else AIMessage(content=row.message)
            for row in rows
        ]
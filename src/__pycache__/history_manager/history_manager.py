from redis_manager import RedisManager

class HistoryManager:
    def __init__(self):
        self.redis = RedisManager()

    def save_message(self, session_id: str, role: str, message: str, metadata=None):
        self.redis.add_message(session_id, role, message, metadata)

    def flush_session(self, session_id: str):
        self.redis.flush_to_postgres(session_id)
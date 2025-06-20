import redis
import json
from datetime import datetime
from db import ChatHistory
import uuid

class RedisManager:
    def __init__(self, host='localhost', port=6379, db=0, ttl=259200):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.ttl = ttl

    def add_message(self, session_id: str, role: str, message: str, metadata=None):
        key = f"chat:{session_id}"
        payload = {
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat(),
            "role": role,
            "message": message,
            "metadata": metadata or {}
        }
        self.client.lpush(key, json.dumps(payload))
        self.client.ltrim(key, 0, 9)
        self.client.expire(key, self.ttl)

    def flush_to_postgres(self, session_id: str):
        key = f"chat:{session_id}"
        messages = self.client.lrange(key, 0, -1)
        for msg_str in reversed(messages):
            msg = json.loads(msg_str)
            ChatHistory.create(
                session_id=uuid.UUID(msg['session_id']),
                timestamp=datetime.fromisoformat(msg['timestamp']),
                role=msg['role'],
                message=msg['message'],
                metadata=msg['metadata']
            )
        self.client.delete(key)
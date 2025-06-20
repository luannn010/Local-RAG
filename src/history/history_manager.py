import redis
from peewee import Model, TextField, SqliteDatabase, DateTimeField
from datetime import datetime
import json
import os

# Setup Redis
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Setup Peewee + PostgreSQL
from playhouse.postgres_ext import PostgresqlExtDatabase

pg_db = PostgresqlExtDatabase(
    os.getenv("DB_POSTGRESDB_DATABASE", "n8n"),
    user=os.getenv("DB_POSTGRESDB_USER", "n8n"),
    password=os.getenv("DB_POSTGRESDB_PASSWORD", "n8n"),
    host=os.getenv("DB_POSTGRESDB_HOST", "localhost"),
    port=int(os.getenv("DB_POSTGRESDB_PORT", 5432)),
)

# Define Peewee model
class ChatHistory(Model):
    session_id = TextField()
    role = TextField()
    content = TextField()
    timestamp = DateTimeField(default=datetime.utcnow)

    class Meta:
        database = pg_db

pg_db.connect()
pg_db.create_tables([ChatHistory], safe=True)

# HistoryManager
class HistoryManager:
    MAX_REDIS_MESSAGES = 10
    REDIS_EXPIRE_SECONDS = 3 * 24 * 60 * 60  # 3 days

    @staticmethod
    def _redis_key(session_id):
        return f"chat:{session_id}"

    @classmethod
    def save_to_redis(cls, session_id: str, role: str, content: str):
        key = cls._redis_key(session_id)
        msg = json.dumps({"role": role, "content": content, "timestamp": datetime.utcnow().isoformat()})
        redis_client.rpush(key, msg)
        redis_client.expire(key, cls.REDIS_EXPIRE_SECONDS)
        # Keep only last 10 messages
        redis_client.ltrim(key, -cls.MAX_REDIS_MESSAGES, -1)

    @classmethod
    def flush_to_postgres(cls, session_id: str):
        key = cls._redis_key(session_id)
        messages = redis_client.lrange(key, 0, -1)
        for msg_str in messages:
            msg = json.loads(msg_str)
            ChatHistory.create(
                session_id=session_id,
                role=msg["role"],
                content=msg["content"],
                timestamp=datetime.fromisoformat(msg["timestamp"])
            )
        redis_client.delete(key)

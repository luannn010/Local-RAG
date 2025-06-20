import redis
from peewee import Model, TextField, DateTimeField
from playhouse.postgres_ext import PostgresqlExtDatabase
from datetime import datetime
import json
import os
import psycopg2  # For creating the database if it doesn't exist

# Setup Redis
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Ensure the database exists
def ensure_database_exists():
    db_name = os.getenv("DB_POSTGRESDB_DATABASE", "local_rag")
    db_user = os.getenv("DB_POSTGRESDB_USER", "postgres")
    db_password = os.getenv("DB_POSTGRESDB_PASSWORD", "postgres-password")
    db_host = os.getenv("DB_POSTGRESDB_HOST", "localhost")
    db_port = int(os.getenv("DB_POSTGRESDB_PORT", 5432))

    try:
        # Connect to the default 'postgres' database to check/create the target database
        conn = psycopg2.connect(
            dbname="postgres",
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Database '{db_name}' created successfully.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error ensuring database exists: {e}")

# Ensure the database exists before connecting
ensure_database_exists()

# Setup Peewee + PostgreSQL
pg_db = PostgresqlExtDatabase(
    os.getenv("DB_POSTGRESDB_DATABASE", "local_rag"),
    user=os.getenv("DB_POSTGRESDB_USER", "postgres"),
    password=os.getenv("DB_POSTGRESDB_PASSWORD", "postgres-password"),
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

# Connect to the database and create the table if it doesn't exist
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

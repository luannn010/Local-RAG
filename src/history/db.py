from peewee import (
    Model, PostgresqlDatabase, UUIDField, TextField, DateTimeField
)
from datetime import datetime
from playhouse.postgres_ext import PostgresqlExtDatabase, JSONField
import os

pg_db = PostgresqlExtDatabase(
    os.getenv("DB_POSTGRESDB_DATABASE", "n8n"),
    user=os.getenv("DB_POSTGRESDB_USER", "n8n"),
    password=os.getenv("DB_POSTGRESDB_PASSWORD", "n8n"),
    host=os.getenv("DB_POSTGRESDB_HOST", "localhost"),
    port=int(os.getenv("DB_POSTGRESDB_PORT", 5432)),
)
class BaseModel(Model):
    class Meta:
        database = pg_db

class ChatHistory(BaseModel):
    session_id = UUIDField()
    timestamp = DateTimeField(default=datetime.utcnow)
    role = TextField()
    message = TextField()
    metadata = JSONField(null=True)

def init_db():
    pg_db.connect()
    pg_db.create_tables([ChatHistory])
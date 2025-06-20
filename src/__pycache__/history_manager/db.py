from peewee import (
    Model, PostgresqlDatabase, UUIDField, TextField, DateTimeField, JSONField
)
from datetime import datetime

pg_db = PostgresqlDatabase(
    'chatdb', user='postgres', password='password', host='localhost', port=5432
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
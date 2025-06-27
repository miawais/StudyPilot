from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.types import JSON
from datetime import datetime
from app.db.database import Base

class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    query = Column(Text)
    response = Column(Text)
    chunk_metadata = Column(JSON)  
    timestamp = Column(DateTime, default=datetime.utcnow)


from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.types import JSON
from datetime import datetime
from app.db.database import Base

class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True) 
    username=Column(String,index=True) #to track user name in chat logs
    query = Column(Text)
    response = Column(Text)
    chunk_metadata = Column(JSON)  
    timestamp = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

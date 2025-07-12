from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Optional: For reverse relationship from User to ChatLog
    chat_logs = relationship("ChatLog", back_populates="user")


class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)  # ✅ Correct FK
    username = Column(String, index=True)  # Still useful for logs, but optional
    query = Column(Text)
    response = Column(Text)
    chunk_metadata = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # ✅ Establish relationship to User
    user = relationship("User", back_populates="chat_logs")

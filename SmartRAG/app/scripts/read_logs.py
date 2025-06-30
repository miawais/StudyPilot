import sys
import os

# Dynamically set project root so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.db.database import SessionLocal
from app.db.models import ChatLog, User

def read_logs():
    db = SessionLocal()
    # Join ChatLog with User to fetch the username
    logs = (
        db.query(ChatLog, User.username)
        .join(User, ChatLog.user_id == User.id, isouter=True)
        .order_by(ChatLog.timestamp.desc())
        .all()
    )

    if not logs:
        print("⚠️ No chat logs found.")
        return

    for log, username in logs:
        user_display = username if username else "🕵️ Unknown User"
        print(f"🧾 {log.timestamp} | 🧑 {user_display} | 🗨️ {log.query}")
        print(f"🤖 Response: {log.response[:200]}...")  # Limit response length for clarity
        print(f"📎 Metadata: {log.chunk_metadata}")
        print("-" * 80)

if __name__ == "__main__":
    read_logs()

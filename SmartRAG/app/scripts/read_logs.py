import sys
import os

#Dynamically set project root so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.db.database import SessionLocal
from app.db.models import ChatLog

def read_logs():
    db = SessionLocal()
    logs = db.query(ChatLog).order_by(ChatLog.timestamp.desc()).all()

    if not logs:
        print("📭 No chat logs found.")
        return

    for log in logs:
        print(f"🧾 {log.timestamp} | {log.user_id}: {log.query}")
        print(f"🤖 Response: {log.response[:120]}...")
        print(f"📎 Metadata: {log.metadata}")
        print("-" * 50)

if __name__ == "__main__":
    read_logs()

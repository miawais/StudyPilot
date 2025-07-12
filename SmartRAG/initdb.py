from app.db.database import Base, engine, SessionLocal
from app.db.models import User, ChatLog
from app.auth.auth_utils import hash_password
from datetime import datetime

# Create tables
Base.metadata.drop_all(bind=engine)  # Optional: reset DB
Base.metadata.create_all(bind=engine)

# Add sample users and logs
def seed_data():
    db = SessionLocal()

    # Create a sample user
    user = User(username="awais", hashed_password=hash_password("test123"))
    db.add(user)
    db.commit()
    db.refresh(user)  # ✅ get the user.id

    # Create a sample chat log tied to the user
    chat = ChatLog(
        user_id=user.id,
        username=user.username,  # still good for logs
        query="What is problem solving?",
        response="Problem solving is the process of identifying a problem and finding a solution.",
        chunk_metadata=[
            {
                "chapter": "Unit 1: Problem Solving",
                "topic": "Introduction",
                "subtopic": "1.1 Overview",
                "type": "definition",
                "score": 0.9
            }
        ],
        timestamp=datetime.utcnow()
    )
    db.add(chat)
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_data()

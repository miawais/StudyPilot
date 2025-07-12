from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict
from sqlalchemy.orm import Session
from collections import Counter

from app.services.chat_services import process_query
from app.services.dependencies import get_current_user, get_db
from app.db.models import User, ChatLog

router = APIRouter(prefix="/api", tags=["Chatbot + Analytics"])  # 👈 centralized prefixing

# ------------------------------
# Chatbot Ask Endpoint
# ------------------------------
class AskRequest(BaseModel):
    query: str
    history: List[Dict] = []

@router.post("/ask")
async def ask_question(
    request: AskRequest,
    user: User = Depends(get_current_user)
):
    result = process_query(
        user_query=request.query,
        user=user,
        chat_history=request.history
    )
    return result

# ------------------------------
# Analytics Endpoints
# ------------------------------
@router.get("/top-chapters")
async def get_top_chapters(db: Session = Depends(get_db)):
    logs = db.query(ChatLog).all()
    chapter_counter = Counter()
    for log in logs:
        for meta in log.chunk_metadata or []:
            if chapter := meta.get("chapter"):
                chapter_counter[chapter] += 1
    return {"top_chapters": chapter_counter.most_common(5)}

@router.get("/most-used-keywords")
def most_used_keywords(db: Session = Depends(get_db)):
    logs = db.query(ChatLog).all()
    word_counter = Counter()
    stopwords = {"the", "is", "a", "an", "and", "to", "in", "of", "that", "what", "how", "tell", "me"}

    for log in logs:
        words = log.query.lower().split()
        filtered = [word.strip(".,?!") for word in words if word not in stopwords and len(word) > 2]
        word_counter.update(filtered)

    return {"most_used_keywords": word_counter.most_common(10)}

@router.get("/daily-activity")
def get_daily_activity(db: Session = Depends(get_db)):
    logs = db.query(ChatLog).all()
    activity = Counter()
    for log in logs:
        day = log.timestamp.date()
        activity[day] += 1
    return {"daily_activity": sorted(activity.items())}

@router.get("/user-activity")
def get_user_activity(db: Session = Depends(get_db)):
    logs = db.query(ChatLog).all()
    user_counter = Counter()
    for log in logs:
        user_counter[log.username or "Unknown"] += 1
    return {"user_activity": user_counter.most_common(10)}

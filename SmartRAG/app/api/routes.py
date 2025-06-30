from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict

from app.services.chat_services import process_query
from app.services.dependencies import get_current_user
from app.db.models import User

router = APIRouter()

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

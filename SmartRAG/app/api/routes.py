from fastapi import APIRouter, Request
from pydantic import BaseModel
from services.chat_service import process_query

router = APIRouter()

class AskRequest(BaseModel):
    user_id: str
    query: str
    history: list[dict] = []  

@router.post("/ask")
async def ask_question(request: AskRequest):
    result = process_query(
        user_query=request.query,
        user_id=request.user_id,
        chat_history=request.history
    )
    return result

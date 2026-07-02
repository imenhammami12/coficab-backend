from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.deps import get_current_user
from app.models.user import User
from app.rag.chatbot import ask_chatbot

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


@router.post("/ask", response_model=ChatResponse)
def ask(request: ChatRequest, _: User = Depends(get_current_user)):
    result = ask_chatbot(request.question)
    return result
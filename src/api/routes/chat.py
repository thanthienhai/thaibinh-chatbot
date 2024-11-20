from fastapi import APIRouter, Depends
from src.models.schemas import ChatRequest, ChatResponse
from src.services.chat_service import ChatService
from src.api.deps import get_chat_service

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    return await chat_service.get_answer(request)
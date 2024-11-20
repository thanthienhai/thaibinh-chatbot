from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    role: str
    content: str

class ChatHistory(BaseModel):
    messages: List[Message]

class ChatRequest(BaseModel):
    message: str
    history: Optional[ChatHistory]

class ChatResponse(BaseModel):
    answer: str
    context: Optional[str]

class Document(BaseModel):
    content: str
    metadata: Optional[dict]
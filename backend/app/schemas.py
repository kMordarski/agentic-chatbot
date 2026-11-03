import uuid
from typing import Literal
from pydantic import BaseModel

class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    
class ChatRequest(BaseModel):
    messages: list[Message]
    conversation_id: uuid.UUID

class ChatResponse(BaseModel):
    reply: str
    

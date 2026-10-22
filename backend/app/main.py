from typing import Annotated
from fastapi import Depends, FastAPI
from app.settings import settings
from app.schemas import ChatRequest, ChatResponse
from app.llm import get_reply

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok", "model_name": settings.model_name}

@app.post("/chat")
async def chat(request: ChatRequest):
    return ChatResponse(reply=await get_reply(request.messages))
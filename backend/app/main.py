from typing import Annotated
from app.settings import settings
from fastapi import Depends, FastAPI
from app.schemas import ChatRequest, ChatResponse

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok", "model_name": settings.model_name}

@app.post("/chat")
async def chat(request: ChatRequest):
    return ChatResponse(reply=f"Echo: {request.messages[-1].content}")
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.settings import settings, frontend_origin
from app.schemas import ChatRequest, ChatResponse
from app.llm import get_reply

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "model_name": settings.model_name}

@app.post("/chat")
async def chat(request: ChatRequest):
    return ChatResponse(reply=await get_reply(request.messages))
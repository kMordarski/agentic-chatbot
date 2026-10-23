from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.llm import AnthropicLLM, get_llm
from app.settings import settings, frontend_origin
from app.schemas import ChatRequest, ChatResponse

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
async def chat(request: ChatRequest,
               llm: Annotated[AnthropicLLM,
                              Depends(get_llm)]):
    return ChatResponse(reply=await llm.reply(request.messages))
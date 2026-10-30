import json
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from app.llm import AnthropicLLM, get_llm
from app.settings import settings
from app.schemas import ChatRequest, ChatResponse
from app.auth import verify_api_key

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.frontend_origin,
    allow_methods=['GET', 'POST'],
    allow_headers=['Content-Type', 'X-API-Key'],
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "model_name": settings.model_name}

@app.post("/chat", dependencies=[Depends(verify_api_key)])
async def chat(request: ChatRequest,
               llm: Annotated[AnthropicLLM,
                              Depends(get_llm)]):
    return ChatResponse(reply=await llm.reply(request.messages))

@app.post("/chat/stream", dependencies=[Depends(verify_api_key)])
async def chat_stream(request: ChatRequest,
                    llm: Annotated[AnthropicLLM,
                                   Depends(get_llm)]):
    async def event_gen():
        
        async for chunk in llm.stream(request.messages):
            
            yield f"data: {json.dumps(chunk)}\n\n"
            
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(event_gen(), 
                             media_type="text/event-stream", 
                             headers={"Cache-Control": "no-cache"})

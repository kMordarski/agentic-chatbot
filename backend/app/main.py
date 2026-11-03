import json
import uuid
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from app.llm import AnthropicLLM, get_llm
from app.settings import settings
from app.schemas import ChatRequest, ChatResponse
from app.auth import verify_api_key
from app.db import get_session, SessionLocal
from app.models import Conversation, MessageRow

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

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
                                   Depends(get_llm)],
                    session: AsyncSession = Depends(get_session)):
    
    usr_msg = request.messages[-1]
    usr_to_save = MessageRow(conversation_id = request.conversation_id, 
                             role = "user", 
                             content = usr_msg.content)
    
    session.add(usr_to_save)
    await session.commit()
    
    async def event_gen():
        
        list_msg = []
        
        async for chunk in llm.stream(request.messages):
            
            list_msg.append(chunk)
            
            yield f"data: {json.dumps(chunk)}\n\n"
        
        async with SessionLocal() as s:
            ass_to_save = MessageRow(conversation_id = request.conversation_id,
                                     role = "assistant",
                                     content = "".join(list_msg))
            s.add(ass_to_save)
            await s.commit()
        
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(event_gen(), 
                            media_type="text/event-stream", 
                            headers={"Cache-Control": "no-cache"})

@app.post("/conversations", dependencies=[Depends(verify_api_key)])
async def create_conversation(session: AsyncSession = Depends(get_session)):
    conv = Conversation()
    session.add(conv)
    await session.commit()
    return {"id": str(conv.id)}

@app.get("/conversations/{conversation_id}/messages", dependencies=[Depends(verify_api_key)])
async def get_messages(conversation_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    stmt = (
        select(MessageRow)
        .where(MessageRow.conversation_id == conversation_id)
        .order_by(MessageRow.id)
    )
    result = await session.execute(stmt)
    rows = result.scalars().all()
    return [{"role": r.role, "content": r.content} for r in rows]
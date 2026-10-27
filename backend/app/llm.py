from anthropic import AsyncAnthropic

from app.settings import settings
from app.schemas import Message
from collections.abc import AsyncIterator
from functools import lru_cache

SYSTEM_PROMPT = "you are a helpful assistant"

class AnthropicLLM:
    def __init__(self):
        self.client = AsyncAnthropic(api_key = settings.anthropic_api_key.get_secret_value())
        
    async def reply(self, messages: list[Message]) -> str:
        response = await self.client.messages.create(
                model=settings.model_name,
                max_tokens=settings.max_tokens,
                system=SYSTEM_PROMPT,
                messages=[m.model_dump() for m in messages]
            )
        return response.content[0].text

    async def stream(self, messages: list[Message]) -> AsyncIterator[str]:
        async with self.client.messages.stream(
                model=settings.model_name,
                max_tokens=settings.max_tokens,
                system=SYSTEM_PROMPT,
                messages=[m.model_dump() for m in messages]            
            ) as s:
        
            async for chunk in s.text_stream:
                            
                yield chunk

@lru_cache
def get_llm() -> AnthropicLLM:
    return AnthropicLLM()

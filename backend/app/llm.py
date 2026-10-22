from anthropic import AsyncAnthropic

from app.settings import settings
from app.schemas import Message

client = AsyncAnthropic(api_key = settings.anthropic_api_key.get_secret_value())

SYSTEM_PROMPT = "you are a helpful assistant"

async def get_reply(messages: list[Message]) -> str:
    response = await client.messages.create(
        model=settings.model_name,
        max_tokens=settings.max_tokens,
        system=SYSTEM_PROMPT,
        messages=[m.model_dump() for m in messages]
    )
    return response.content[0].text


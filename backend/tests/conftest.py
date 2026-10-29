import os

os.environ.setdefault('APP_API_KEY', 'test-key')
os.environ.setdefault('MODEL_NAME', 'claude-haiku-5-5')
os.environ.setdefault('MAX_TOKENS', '1024')
os.environ.setdefault('ANTHROPIC_API_KEY', 'test-andthropic-key')

from app.settings import settings
from app.main import app
from pydantic import SecretStr
from app.schemas import Message



class FakeLLM:
    def __init__(self):
        self.client = 'fake_key'
        
    async def reply(self, messages: list[Message]) -> str:
        response = await self.client.messages.create(
                model=settings.model_name,
                max_tokens=settings.max_tokens,
                system=SYSTEM_PROMPT,
                messages=[m.model_dump() for m in messages]
            )
        return 'example_text'

    async def stream(self, messages: list[Message]):
        while messages:
            yield messages
        

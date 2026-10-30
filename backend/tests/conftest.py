import os

os.environ.setdefault("APP_API_KEY", "test-key")
os.environ.setdefault("MODEL_NAME", "claude-haiku-5-5")
os.environ.setdefault("MAX_TOKENS", "1024")
os.environ.setdefault("ANTHROPIC_API_KEY", "test-anthropic-key")

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.llm import get_llm
from app.schemas import Message


class FakeLLM:
    async def reply(self, messages: list[Message]) -> str:
        return "fixed_string"

    async def stream(self, messages: list[Message]):
        for item in ["hel", "lo", "!"]:
            yield item


@pytest.fixture
def client():
    app.dependency_overrides[get_llm] = lambda: FakeLLM()
    yield TestClient(app)
    app.dependency_overrides.clear()
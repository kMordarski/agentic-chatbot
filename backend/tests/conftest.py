import os
 
os.environ.setdefault("APP_API_KEY", "test-key")
os.environ.setdefault("MODEL_NAME", "claude-haiku-5-5")
os.environ.setdefault("MAX_TOKENS", "1024")
os.environ.setdefault("ANTHROPIC_API_KEY", "test-anthropic-key")
os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://test:test@localhost:5432/test")
 
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
 
import app.main as main_module
import app.models  # noqa: F401  (registers the tables on Base.metadata)
from app.db import Base, get_session
from app.llm import get_llm
from app.main import app
from app.schemas import Message
 
HEADERS = {"X-API-Key": "test-key"}
 
 
class FakeLLM:
    async def reply(self, messages: list[Message]) -> str:
        return "fixed_string"
 
    async def stream(self, messages: list[Message]):
        for item in ["hel", "lo", "!"]:
            yield item
 
 
@pytest.fixture
def client(monkeypatch):
    # A fresh in-memory SQLite database for every test.
    # StaticPool = every session shares ONE connection, otherwise each
    # connection would get its own empty in-memory database.
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestSession = async_sessionmaker(engine, expire_on_commit=False)
 
    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
 
    async def override_get_session():
        async with TestSession() as session:
            yield session
 
    # Routes that use Depends(get_session) get the SQLite session...
    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_llm] = lambda: FakeLLM()
    # ...and the stream generator, which opens SessionLocal() directly,
    # gets the SQLite session factory too.
    monkeypatch.setattr(main_module, "SessionLocal", TestSession)
 
    # "with" keeps one event loop for the whole test, so the shared
    # SQLite connection is always used from the same loop.
    with TestClient(app) as c:
        c.portal.call(create_tables)
        yield c
        c.portal.call(engine.dispose)
 
    app.dependency_overrides.clear()
 
 
@pytest.fixture
def conversation_id(client):
    response = client.post("/conversations", headers=HEADERS)
    return response.json()["id"]
 
import asyncio
from app.llm import get_llm
from app.schemas import Message

async def main():
    async for piece in get_llm().stream([Message(role="user", content="Count to 20")]):
        print(repr(piece), flush=True)

asyncio.run(main())
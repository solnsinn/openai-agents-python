"""AsyncOpenAI client shim"""
import asyncio
from typing import Any

class AsyncOpenAI:
    def __init__(self, *args, **kwargs):
        # store a base_url attribute to mirror the upstream client's surface
        self.base_url = kwargs.get("base_url", "https://api.openai.com")

    def __repr__(self) -> str:  # helpful when printed in tests
        return f"<AsyncOpenAI base_url={self.base_url}>"

    async def chat_completions(self, *args, **kwargs) -> Any:
        await asyncio.sleep(0)
        return {"choices": [{"message": {"content": "(shim) chat response"}}]}

    async def responses(self, *args, **kwargs) -> Any:
        await asyncio.sleep(0)
        return {"output": "(shim) responses"}

__all__ = ["AsyncOpenAI"]

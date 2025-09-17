from __future__ import annotations

from typing import Optional

try:
    from pydantic import BaseModel


    class PromptTokensDetails(BaseModel):
        cached_tokens: Optional[int] = None


    class CompletionTokensDetails(BaseModel):
        reasoning_tokens: Optional[int] = None


    class OutputTokensDetails(BaseModel):
        reasoning_tokens: Optional[int] = None


    class CompletionUsage(BaseModel):
        completion_tokens: Optional[int] = None
        prompt_tokens: Optional[int] = None
        total_tokens: Optional[int] = None
        completion_tokens_details: Optional[CompletionTokensDetails] = None
        prompt_tokens_details: Optional[PromptTokensDetails] = None

except Exception:
    # Fallback permissive attribute containers if pydantic isn't available.
    class PromptTokensDetails:
        def __init__(self, cached_tokens: int | None = None):
            self.cached_tokens = cached_tokens


    class CompletionTokensDetails:
        def __init__(self, reasoning_tokens: int | None = None):
            self.reasoning_tokens = reasoning_tokens


    class OutputTokensDetails:
        def __init__(self, reasoning_tokens: int | None = None):
            self.reasoning_tokens = reasoning_tokens


    class CompletionUsage:
        def __init__(
            self,
            completion_tokens: int | None = None,
            prompt_tokens: int | None = None,
            total_tokens: int | None = None,
            completion_tokens_details: object | None = None,
            prompt_tokens_details: object | None = None,
        ) -> None:
            self.completion_tokens = completion_tokens
            self.prompt_tokens = prompt_tokens
            self.total_tokens = total_tokens
            self.completion_tokens_details = completion_tokens_details
            self.prompt_tokens_details = prompt_tokens_details


__all__ = ["CompletionUsage", "PromptTokensDetails", "CompletionTokensDetails", "OutputTokensDetails"]

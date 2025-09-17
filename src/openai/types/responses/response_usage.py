from __future__ import annotations

from typing import Optional

try:
    from pydantic import BaseModel

    class InputTokensDetails(BaseModel):
        cached_tokens: Optional[int] = None


    class OutputTokensDetails(BaseModel):
        reasoning_tokens: Optional[int] = None


    class ResponseUsage(BaseModel):
        input_tokens: Optional[int] = None
        output_tokens: Optional[int] = None
        total_tokens: Optional[int] = None
        input_tokens_details: Optional[InputTokensDetails] = None
        output_tokens_details: Optional[OutputTokensDetails] = None

except Exception:
    class InputTokensDetails:
        def __init__(self, cached_tokens: int | None = None):
            self.cached_tokens = cached_tokens


    class OutputTokensDetails:
        def __init__(self, reasoning_tokens: int | None = None):
            self.reasoning_tokens = reasoning_tokens


    class ResponseUsage:
        def __init__(
            self,
            input_tokens: int | None = None,
            output_tokens: int | None = None,
            total_tokens: int | None = None,
            input_tokens_details: Any | None = None,
            output_tokens_details: Any | None = None,
        ) -> None:
            self.input_tokens = input_tokens
            self.output_tokens = output_tokens
            self.total_tokens = total_tokens
            self.input_tokens_details = input_tokens_details
            self.output_tokens_details = output_tokens_details

__all__ = ["InputTokensDetails", "OutputTokensDetails", "ResponseUsage"]

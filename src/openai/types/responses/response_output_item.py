from __future__ import annotations

from typing import Any, Optional

try:
    from pydantic import BaseModel

    class ImageGenerationCall(BaseModel):
        prompt: Optional[str] = None


    class LocalShellCall(BaseModel):
        command: Optional[str] = None
        exit_code: Optional[int] = None
        output: Optional[str] = None


    class McpApprovalRequest(BaseModel):
        request_id: Optional[str] = None
        details: Optional[Any] = None


    class McpCall(BaseModel):
        call: Optional[Any] = None


    class McpListTools(BaseModel):
        tools: Optional[list[Any]] = None

except Exception:
    class ImageGenerationCall:
        def __init__(self, prompt: Any = None):
            self.prompt = prompt


    class LocalShellCall:
        def __init__(self, command: Any = None, exit_code: Any = None, output: Any = None):
            self.command = command
            self.exit_code = exit_code
            self.output = output


    class McpApprovalRequest:
        def __init__(self, request_id: Any = None, details: Any = None):
            self.request_id = request_id
            self.details = details


    class McpCall:
        def __init__(self, call: Any = None):
            self.call = call


    class McpListTools:
        def __init__(self, tools: Any = None):
            self.tools = tools


__all__ = [
    "ImageGenerationCall",
    "LocalShellCall",
    "McpApprovalRequest",
    "McpCall",
    "McpListTools",
]

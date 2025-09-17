from __future__ import annotations

from typing import Any, Optional

try:
    from pydantic import BaseModel

    class ResponseInputItemParam(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        default: Optional[Any] = None


    class ComputerCallOutput(BaseModel):
        output: Optional[Any] = None


    class ComputerCallOutputAcknowledgedSafetyCheck(BaseModel):
        acknowledged: Optional[bool] = None


    class FunctionCallOutput(BaseModel):
        function: Optional[str] = None
        args: Optional[dict] = None


    class LocalShellCallOutput(BaseModel):
        command: Optional[str] = None
        exit_code: Optional[int] = None
        output: Optional[str] = None


    class McpApprovalResponse(BaseModel):
        approved: Optional[bool] = None
        reason: Optional[str] = None

except Exception:
    class ResponseInputItemParam:
        def __init__(self, name: Any = None, description: Any = None, default: Any = None):
            self.name = name
            self.description = description
            self.default = default


    class ComputerCallOutput:
        def __init__(self, output: Any = None):
            self.output = output


    class ComputerCallOutputAcknowledgedSafetyCheck:
        def __init__(self, acknowledged: Any = None):
            self.acknowledged = acknowledged


    class FunctionCallOutput:
        def __init__(self, function: Any = None, args: Any = None):
            self.function = function
            self.args = args


    class LocalShellCallOutput:
        def __init__(self, command: Any = None, exit_code: Any = None, output: Any = None):
            self.command = command
            self.exit_code = exit_code
            self.output = output


    class McpApprovalResponse:
        def __init__(self, approved: Any = None, reason: Any = None):
            self.approved = approved
            self.reason = reason


__all__ = [
    "ResponseInputItemParam",
    "ComputerCallOutput",
    "ComputerCallOutputAcknowledgedSafetyCheck",
    "FunctionCallOutput",
    "LocalShellCallOutput",
    "McpApprovalResponse",
]

from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic, Literal, TypeVar, Union

import pydantic
from openai.types.responses import (
    Response,
    ResponseComputerToolCall,
    ResponseFileSearchToolCall,
    ResponseFunctionToolCall,
    ResponseFunctionWebSearch,
    ResponseInputItemParam,
    ResponseOutputItem,
    ResponseOutputMessage,
    ResponseOutputRefusal,
    ResponseOutputText,
    ResponseStreamEvent,
)
from openai.types.responses.response_code_interpreter_tool_call import (
    ResponseCodeInterpreterToolCall,
)
from openai.types.responses.response_input_item_param import (
    ComputerCallOutput,
    FunctionCallOutput,
    LocalShellCallOutput,
    McpApprovalResponse,
)
from openai.types.responses.response_output_item import (
    ImageGenerationCall,
    LocalShellCall,
    McpApprovalRequest,
    McpCall,
    McpListTools,
)
from openai.types.responses.response_reasoning_item import ResponseReasoningItem
from pydantic import BaseModel
from typing_extensions import TypeAlias

from .exceptions import AgentsException, ModelBehaviorError
from .usage import Usage

if TYPE_CHECKING:
    from .agent import Agent

TResponse = Response
"""A type alias for the Response type from the OpenAI SDK."""

TResponseInputItem = ResponseInputItemParam
"""A type alias for the ResponseInputItemParam type from the OpenAI SDK."""

TResponseOutputItem = ResponseOutputItem
"""A type alias for the ResponseOutputItem type from the OpenAI SDK."""

TResponseStreamEvent = ResponseStreamEvent
"""A type alias for the ResponseStreamEvent type from the OpenAI SDK."""

T = TypeVar("T", bound=Union[TResponseOutputItem, TResponseInputItem])


@dataclass
class RunItemBase(Generic[T], abc.ABC):
    agent: Agent[Any]
    """The agent whose run caused this item to be generated."""

    raw_item: T
    """The raw Responses item from the run. This will always be either an output item (i.e.
    `openai.types.responses.ResponseOutputItem` or an input item
    (i.e. `openai.types.responses.ResponseInputItemParam`).
    """

    def to_input_item(self) -> TResponseInputItem:
        """Converts this item into an input item suitable for passing to the model."""
        if isinstance(self.raw_item, dict):
            # We know that input items are dicts, so we can ignore the type error
            return self.raw_item  # type: ignore
        elif isinstance(self.raw_item, BaseModel):
            # All output items are Pydantic models that can be converted to input items.
            return self.raw_item.model_dump(exclude_unset=True)  # type: ignore
        else:
            raise AgentsException(f"Unexpected raw item type: {type(self.raw_item)}")


@dataclass
class MessageOutputItem(RunItemBase[ResponseOutputMessage]):
    """Represents a message from the LLM."""

    raw_item: ResponseOutputMessage
    """The raw response output message."""

    type: Literal["message_output_item"] = "message_output_item"


@dataclass
class HandoffCallItem(RunItemBase[ResponseFunctionToolCall]):
    """Represents a tool call for a handoff from one agent to another."""

    raw_item: ResponseFunctionToolCall
    """The raw response function tool call that represents the handoff."""

    type: Literal["handoff_call_item"] = "handoff_call_item"


@dataclass
class HandoffOutputItem(RunItemBase[TResponseInputItem]):
    """Represents the output of a handoff."""

    raw_item: TResponseInputItem
    """The raw input item that represents the handoff taking place."""

    source_agent: Agent[Any]
    """The agent that made the handoff."""

    target_agent: Agent[Any]
    """The agent that is being handed off to."""

    type: Literal["handoff_output_item"] = "handoff_output_item"


ToolCallItemTypes: TypeAlias = Union[
    ResponseFunctionToolCall,
    ResponseComputerToolCall,
    ResponseFileSearchToolCall,
    ResponseFunctionWebSearch,
    McpCall,
    ResponseCodeInterpreterToolCall,
    ImageGenerationCall,
    LocalShellCall,
]
"""A type that represents a tool call item."""


@dataclass
class ToolCallItem(RunItemBase[ToolCallItemTypes]):
    """Represents a tool call e.g. a function call or computer action call."""

    raw_item: ToolCallItemTypes
    """The raw tool call item."""

    type: Literal["tool_call_item"] = "tool_call_item"


@dataclass
class ToolCallOutputItem(
    RunItemBase[Union[FunctionCallOutput, ComputerCallOutput, LocalShellCallOutput]]
):
    """Represents the output of a tool call."""

    raw_item: FunctionCallOutput | ComputerCallOutput | LocalShellCallOutput
    """The raw item from the model."""

    output: Any
    """The output of the tool call. This is whatever the tool call returned; the `raw_item`
    contains a string representation of the output.
    """

    type: Literal["tool_call_output_item"] = "tool_call_output_item"


@dataclass
class ReasoningItem(RunItemBase[ResponseReasoningItem]):
    """Represents a reasoning item."""

    raw_item: ResponseReasoningItem
    """The raw reasoning item."""

    type: Literal["reasoning_item"] = "reasoning_item"


@dataclass
class MCPListToolsItem(RunItemBase[McpListTools]):
    """Represents a call to an MCP server to list tools."""

    raw_item: McpListTools
    """The raw MCP list tools call."""

    type: Literal["mcp_list_tools_item"] = "mcp_list_tools_item"


@dataclass
class MCPApprovalRequestItem(RunItemBase[McpApprovalRequest]):
    """Represents a request for MCP approval."""

    raw_item: McpApprovalRequest
    """The raw MCP approval request."""

    type: Literal["mcp_approval_request_item"] = "mcp_approval_request_item"


@dataclass
class MCPApprovalResponseItem(RunItemBase[McpApprovalResponse]):
    """Represents a response to an MCP approval request."""

    raw_item: McpApprovalResponse
    """The raw MCP approval response."""

    type: Literal["mcp_approval_response_item"] = "mcp_approval_response_item"


RunItem: TypeAlias = Union[
    MessageOutputItem,
    HandoffCallItem,
    HandoffOutputItem,
    ToolCallItem,
    ToolCallOutputItem,
    ReasoningItem,
    MCPListToolsItem,
    MCPApprovalRequestItem,
    MCPApprovalResponseItem,
]
"""An item generated by an agent."""


@dataclass
class ModelResponse:
    output: list[Any]
    """A list of outputs (messages, tool calls, etc) generated by the model"""

    usage: Usage
    """The usage information for the response."""

    response_id: str | None
    """An ID for the response which can be used to refer to the response in subsequent calls to the
    model. Not supported by all model providers.
    If using OpenAI models via the Responses API, this is the `response_id` parameter, and it can
    be passed to `Runner.run`.
    """

    def to_input_items(self) -> list[TResponseInputItem]:
        """Convert the output into a list of input items suitable for passing to the model.

        This helper accepts items that are either dict-like, pydantic models (have model_dump),
        or objects with attribute access. It returns a list of plain dicts.
        """
        items: list[TResponseInputItem] = []
        for it in self.output:
            # dict-like
            if isinstance(it, dict):
                items.append(it)
                continue
            # pydantic BaseModel
            if hasattr(it, "model_dump") and callable(getattr(it, "model_dump")):
                items.append(it.model_dump(exclude_unset=True))
                continue
            # objects with attributes (AttrDict-like)
            if hasattr(it, "__dict__"):
                items.append({k: v for k, v in it.__dict__.items()})
                continue
            raise AgentsException(f"Unexpected output item type: {type(it)}")
        return items


class ItemHelpers:
    @classmethod
    def extract_last_content(cls, message: TResponseOutputItem) -> str:
        """Extracts the last text content or refusal from a message."""
        # Accept dicts, pydantic BaseModels, or attribute-access objects.
        if not getattr(message, "content", None):
            return ""

        last_content = message.content[-1]

        # dict-like
        if isinstance(last_content, dict):
            if "text" in last_content:
                return last_content.get("text", "")
            if "refusal" in last_content:
                return last_content.get("refusal", "")
            return ""

        # pydantic BaseModel
        if hasattr(last_content, "model_dump") and callable(getattr(last_content, "model_dump")):
            dumped = last_content.model_dump()
            if isinstance(dumped, dict):
                if "text" in dumped:
                    return dumped.get("text", "")
                if "refusal" in dumped:
                    return dumped.get("refusal", "")
            return ""

        # attribute access
        if hasattr(last_content, "text") and getattr(last_content, "text") is not None:
            return getattr(last_content, "text")
        if hasattr(last_content, "refusal") and getattr(last_content, "refusal") is not None:
            return getattr(last_content, "refusal")

        return ""

    @classmethod
    def extract_last_text(cls, message: TResponseOutputItem) -> str | None:
        """Extracts the last text content from a message, if any. Ignores refusals."""
        if not getattr(message, "content", None):
            return None
        last_content = message.content[-1]

        # dict-like
        if isinstance(last_content, dict):
            return last_content.get("text")

        # pydantic BaseModel
        if hasattr(last_content, "model_dump") and callable(getattr(last_content, "model_dump")):
            dumped = last_content.model_dump()
            if isinstance(dumped, dict):
                return dumped.get("text")

        # attribute access
        if hasattr(last_content, "text"):
            return getattr(last_content, "text")

        return None

    @classmethod
    def input_to_new_input_list(
        cls, input: str | list[TResponseInputItem]
    ) -> list[TResponseInputItem]:
        """Converts a string or list of input items into a list of input items."""
        if isinstance(input, str):
            return [
                {
                    "content": input,
                    "role": "user",
                }
            ]
        return input.copy()

    @classmethod
    def text_message_outputs(cls, items: list[RunItem]) -> str:
        """Concatenates all the text content from a list of message output items."""
        text = ""
        for item in items:
            if isinstance(item, MessageOutputItem):
                text += cls.text_message_output(item)
        return text

    @classmethod
    def text_message_output(cls, message: MessageOutputItem) -> str:
        """Extracts all the text content from a single message output item."""
        parts: list[str] = []
        for item in message.raw_item.content:
            # dict-like
            if isinstance(item, dict) and "text" in item:
                parts.append(item.get("text", ""))
                continue
            # pydantic
            if hasattr(item, "model_dump") and callable(getattr(item, "model_dump")):
                dumped = item.model_dump()
                if isinstance(dumped, dict) and "text" in dumped:
                    parts.append(dumped.get("text", ""))
                continue
            # attribute
            if hasattr(item, "text") and getattr(item, "text") is not None:
                parts.append(getattr(item, "text"))

        return "".join(parts)

    @classmethod
    def tool_call_output_item(
        cls, tool_call: ResponseFunctionToolCall, output: str
    ) -> FunctionCallOutput:
        """Creates a tool call output item from a tool call and its output."""
        return {
            "call_id": tool_call.call_id,
            "output": output,
            "type": "function_call_output",
        }

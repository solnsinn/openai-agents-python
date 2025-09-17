"""Stubs for computer tool call related response types.

Provide small pydantic-friendly classes instead of TypedDicts so the
runtime code can perform isinstance checks and pydantic validation can
accept instances of these shapes.
"""
from __future__ import annotations

from typing import Any, Optional

try:
    from pydantic import BaseModel

    class ResponseComputerToolCall(BaseModel):
        id: Optional[str] = None
        type: Optional[str] = None
        name: Optional[str] = None
        call_id: Optional[str] = None
        action: Optional[Any] = None
        pending_safety_checks: Optional[list[Any]] = None
        status: Optional[str] = None
        output: Optional[Any] = None

    class PendingSafetyCheck(BaseModel):
        check_id: Optional[str] = None
        status: Optional[str] = None

    class ActionClick(BaseModel):
        x: Optional[int] = None
        y: Optional[int] = None
        button: Optional[str] = None

    class ActionWait(BaseModel):
        seconds: Optional[int] = None

    class ActionType(BaseModel):
        # Tests construct ActionType(type="type", text="...")
        type: Optional[str] = None
        text: Optional[str] = None
        params: Optional[dict] = None

    class ActionDoubleClick(BaseModel):
        x: Optional[int] = None
        y: Optional[int] = None
        button: Optional[str] = None

    class ActionRightClick(BaseModel):
        x: Optional[int] = None
        y: Optional[int] = None
        button: Optional[str] = None

    class ActionDrag(BaseModel):
        # Tests construct ActionDrag with a `path` of ActionDragPath(x=.., y=..)
        path: Optional[list["ActionDragPath"]] = None

    class ActionDragPath(BaseModel):
        # Tests expect ActionDragPath(x=..., y=...)
        x: Optional[int] = None
        y: Optional[int] = None

    class ActionScroll(BaseModel):
        # Tests expect fields x, y, scroll_x, scroll_y
        x: Optional[int] = None
        y: Optional[int] = None
        scroll_x: Optional[int] = None
        scroll_y: Optional[int] = None

    class ActionKeypress(BaseModel):
        # Tests expect `keys` (list) and optional `modifiers`
        keys: Optional[list[str]] = None
        modifiers: Optional[list[str]] = None

    class ActionTypeKeyboard(BaseModel):
        type: Optional[str] = None
        keypress: Optional[ActionKeypress] = None

    class ActionMove(BaseModel):
        x: Optional[int] = None
        y: Optional[int] = None

    class ActionTypeMove(BaseModel):
        type: Optional[str] = None
        move: Optional[ActionMove] = None
    class ActionScreenshot(BaseModel):
        region: Optional[dict] = None
        type: Optional[str] = None

    class ActionTypeScreenshot(BaseModel):
        type: Optional[str] = None
        screenshot: Optional[ActionScreenshot] = None
except Exception:
    class ResponseComputerToolCall:
        def __init__(self, name: Any = None, output: Any = None):
            self.name = name
            self.output = output

    class PendingSafetyCheck:
        def __init__(self, check_id: Any = None, status: Any = None):
            self.check_id = check_id
            self.status = status

    class ActionClick:
        def __init__(self, x: Any = None, y: Any = None, button: Any = None):
            self.x = x
            self.y = y
            self.button = button

    class ActionWait:
        def __init__(self, seconds: Any = None):
            self.seconds = seconds

    class ActionType:
        def __init__(self, type: Any = None, text: Any = None, params: Any = None):
            self.type = type
            self.text = text
            self.params = params

    class ActionDoubleClick:
        def __init__(self, x: Any = None, y: Any = None, button: Any = None):
            self.x = x
            self.y = y
            self.button = button

    class ActionRightClick:
        def __init__(self, x: Any = None, y: Any = None, button: Any = None):
            self.x = x
            self.y = y
            self.button = button

    class ActionDrag:
        def __init__(self, path: Any = None, start_x: Any = None, start_y: Any = None, end_x: Any = None, end_y: Any = None):
            # Accept either explicit coordinates or a path list of ActionDragPath-like
            self.path = path
            self.start_x = start_x
            self.start_y = start_y
            self.end_x = end_x
            self.end_y = end_y

    class ActionDragPath:
        def __init__(self, x: Any = None, y: Any = None, points: Any = None):
            # Tests expect x,y attributes
            self.x = x
            self.y = y
            self.points = points

    class ActionScroll:
        def __init__(self, x: Any = None, y: Any = None, scroll_x: Any = None, scroll_y: Any = None, delta_x: Any = None, delta_y: Any = None):
            self.x = x
            self.y = y
            self.scroll_x = scroll_x
            self.scroll_y = scroll_y
            self.delta_x = delta_x
            self.delta_y = delta_y

    class ActionKeypress:
        def __init__(self, keys: Any = None, modifiers: Any = None, key: Any = None):
            # Accept both `keys` (preferred) and legacy `key` single-value
            self.keys = keys
            self.key = key
            self.modifiers = modifiers

    class ActionTypeKeyboard:
        def __init__(self, type: Any = None, keypress: Any = None):
            self.type = type
            self.keypress = keypress

    class ActionMove:
        def __init__(self, x: Any = None, y: Any = None):
            self.x = x
            self.y = y

    class ActionTypeMove:
        def __init__(self, type: Any = None, move: Any = None):
            self.type = type
            self.move = move

    class ActionScreenshot:
        def __init__(self, region: Any = None):
            self.region = region

    class ActionTypeScreenshot:
        def __init__(self, type: Any = None, screenshot: Any = None):
            self.type = type
            self.screenshot = screenshot

__all__ = [
    "ResponseComputerToolCall",
    "PendingSafetyCheck",
    "ActionClick",
    "ActionType",
    "ActionDoubleClick",
    "ActionRightClick",
    "ActionDrag",
    "ActionDragPath",
    "ActionScroll",
    "ActionKeypress",
    "ActionTypeKeyboard",
    "ActionMove",
    "ActionTypeMove",
    "ActionScreenshot",
    "ActionTypeScreenshot",
]

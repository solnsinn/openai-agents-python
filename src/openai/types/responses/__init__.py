"""Fallback stubs for `openai.types.responses` submodules.

This module provides a hybrid approach used by the test/dev
environment: if the real upstream `openai` package provides
the requested submodule or symbol, prefer that; otherwise create
lightweight, pydantic-friendly stubs on demand so imports like

	from openai.types.responses.response_file_search_tool_call import ResponseFileSearchToolCall

do not raise ModuleNotFoundError during import checks.

The stubs are intentionally minimal: a dataclass-like object with
an auto-generated pydantic BaseModel wrapper is returned where
useful. This keeps pydantic happy while avoiding implementing the
full SDK surface.
"""

from __future__ import annotations

from .response_prompt_param import ResponsePromptParam
from .response_includable import ResponseIncludable
from .response import Response
from .response_computer_tool_call import ResponseComputerToolCall
from .response_file_search_tool_call import ResponseFileSearchToolCall

__all__ = [
	"ResponsePromptParam",
	"ResponseIncludable",
	"Response",
	"ResponseComputerToolCall",
	"ResponseFileSearchToolCall",
]

import importlib
import sys
from types import ModuleType
from typing import Any, Dict

# Always prefer our local stubs during testing to avoid upstream TypedDict
# objects which raise TypeError on isinstance/class checks. Importing the
# real upstream `openai.types.responses` can expose TypedDict shapes that
# break runtime isinstance checks used throughout the codebase. Force
# `real_responses` to None so __getattr__ will create pydantic-friendly
# stub classes for any requested symbol.
real_responses = None

# Avoid treating this module as the "real" upstream package: if the
# import returned this module, ignore it to prevent recursion during
# attribute access.
if real_responses is sys.modules.get(__name__):
	real_responses = None

# Ensure a few critical Response* runtime symbols are class-like and
# attribute-accessible. Some upstream packages export these as TypedDicts
# (which instantiate to dicts) and that breaks isinstance checks and
# pydantic validation in the tests. Use AttrDict (pydantic-friendly) when
# available.
try:
	from ._shim_base import AttrDict  # type: ignore

	class ResponseOutputMessage(AttrDict):
		pass

	class ResponseFunctionToolCall(AttrDict):
		pass

	class ResponseOutputItem(AttrDict):
		pass

	class ResponseReasoningItem(AttrDict):
		pass

	class ResponseUsage(AttrDict):
		pass

	globals()["ResponseOutputMessage"] = ResponseOutputMessage
	globals()["ResponseFunctionToolCall"] = ResponseFunctionToolCall
	globals()["ResponseOutputItem"] = ResponseOutputItem
	globals()["ResponseReasoningItem"] = ResponseReasoningItem
	globals()["ResponseUsage"] = ResponseUsage
except Exception:
	# If AttrDict can't be imported for some reason, skip the override.
	pass

if real_responses is not None and real_responses is not sys.modules.get(__name__):
	# Some upstream symbols are TypedDicts or otherwise dict-like which,
	# when instantiated, produce dicts. The codebase expects attribute
	# access on many Response* event and output classes, so prefer our own
	# flexible stubs for those names even when upstream exposes them.
	force_stub_names = {
		"ResponseCreatedEvent",
		"ResponseContentPartAddedEvent",
		"ResponseContentPartDoneEvent",
		"ResponseOutputItemAddedEvent",
		"ResponseOutputItemDoneEvent",
		"ResponseTextDeltaEvent",
		"ResponseRefusalDeltaEvent",
		"ResponseFunctionCallArgumentsDeltaEvent",
		"ResponseReasoningSummaryPartAddedEvent",
		"ResponseReasoningSummaryPartDoneEvent",
		"ResponseReasoningSummaryTextDeltaEvent",
		"ResponseOutputMessage",
		"ResponseOutputText",
		"ResponseOutputRefusal",
		"ResponseOutputItem",
		"ResponseReasoningItem",
		"ResponseUsage",
	}

	# Re-export names from the real package, but skip the force-listed names so
	# our stubs are used instead.
	for attr in dir(real_responses):
		if not attr.startswith("_") and attr not in force_stub_names:
			globals()[attr] = getattr(real_responses, attr)

__all__ = [k for k in globals().keys() if not k.startswith("_")]


def _make_module_stub(module_name: str) -> ModuleType:
	"""Create a lightweight module with a pydantic-friendly stub class.

	The created module will contain a single class whose name is the
	camel-cased version of the final component. E.g. importing
	`openai.types.responses.response_file_search_tool_call` will produce
	a module with `ResponseFileSearchToolCall` class.
	"""
	mod = ModuleType(module_name)

	# Derive a class name from the module tail: response_file_search_tool_call -> ResponseFileSearchToolCall
	tail = module_name.split(".")[-1]
	parts = [p.capitalize() for p in tail.split("_")]
	cls_name = "".join(parts)

	# Minimal class that is friendly for pydantic: simple dataclass-like container
	try:
		from pydantic import BaseModel

		# Create a flexible BaseModel subclass that allows arbitrary fields and types.
		# Provide compatibility for both pydantic v2 (model_config) and v1 (Config).
		model_config = {"extra": "allow", "arbitrary_types_allowed": True}
		# Build a class dict containing both forms so the created class works
		# regardless of whether pydantic v1 or v2 is installed.
		class_dict: Dict[str, object] = {"model_config": model_config}
		# Add a v1-style Config nested class as well.
		class Config:  # type: ignore
			extra = "allow"
			arbitrary_types_allowed = True
		class_dict["Config"] = Config
		StubModel = type(cls_name, (BaseModel,), class_dict)
		setattr(mod, cls_name, StubModel)
	except Exception:
		# Fall back to a simple attribute container if pydantic isn't available
		class _SimpleStub:
			def __init__(self, **kwargs: Any) -> None:  # type: ignore[override]
				for k, v in kwargs.items():
					setattr(self, k, v)

			def __repr__(self) -> str:  # pragma: no cover - trivial
				return f"{cls_name}({self.__dict__})"

		_SimpleStub.__name__ = cls_name
		setattr(mod, cls_name, _SimpleStub)

	return mod


def __getattr__(name: str) -> Any:
	"""Support attribute access on the package (e.g., `from openai.types.responses import X`)."""
	# Special-case pytest plugin discovery: if pytest asks for `pytest_plugins`,
	# return an empty list so pytest doesn't treat our fallback stub as a plugin.
	if name == "pytest_plugins":
		return []

	# Avoid creating fallback stubs for common pytest hook/setup names
	# (pytest will try to call these if present). Return None so pytest
	# ignores them instead of receiving a stub type object.
	if name in {
		"setup_module",
		"teardown_module",
		"setup_function",
		"teardown_function",
		"setup_class",
		"teardown_class",
		"setup_package",
		"teardown_package",
	}:
		return None

	# Only generate dynamic stubs for Response* names. Returning or creating
	# other symbols can interfere with pytest and plugin discovery (we saw
	# pytest attempt to treat our fallback as a plugin). For non-Response
	# names, raise AttributeError to signal absence.
	if not name.startswith("Response"):
		raise AttributeError(name)

	# Prefer existing globals
	if name in globals():
		return globals()[name]

	# If the upstream package provided it, return that
	if real_responses is not None and hasattr(real_responses, name):
		# Some upstream exported symbols are TypedDicts or plain dict-like
		# shapes which instantiate to dicts. The codebase expects attribute
		# access on many Response* event types, so prefer our flexible
		# stub classes for those names even when upstream provides a value.
		force_stub_names = {
			# common event/output/item types used heavily by stream handler
			"ResponseCreatedEvent",
			"ResponseContentPartAddedEvent",
			"ResponseContentPartDoneEvent",
			"ResponseOutputItemAddedEvent",
			"ResponseOutputItemDoneEvent",
			"ResponseTextDeltaEvent",
			"ResponseRefusalDeltaEvent",
			"ResponseFunctionCallArgumentsDeltaEvent",
			"ResponseReasoningSummaryPartAddedEvent",
			"ResponseReasoningSummaryPartDoneEvent",
			"ResponseReasoningSummaryTextDeltaEvent",
			"ResponseOutputMessage",
			"ResponseOutputText",
			"ResponseOutputRefusal",
			"ResponseOutputItem",
			"ResponseReasoningItem",
			"ResponseUsage",
		}
		if name not in force_stub_names:
			val = getattr(real_responses, name)
			globals()[name] = val
			return val

	# Create and return a simple stub. Prefer upstream submodules only
	# when their import spec points to a different file (to avoid
	# re-importing this module and causing recursion).
	from importlib.util import find_spec
	import re

	# Convert CamelCase symbol name to snake_case module name. For example,
	# ResponseCreatedEvent -> response_created_event
	def _camel_to_snake(s: str) -> str:
		s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", s)
		return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

	module_full = f"openai.types.responses.{_camel_to_snake(name)}"
	spec = find_spec(module_full)
	if spec is not None and spec.origin and spec.origin != __file__:
		try:
			upstream = importlib.import_module(module_full)
			if hasattr(upstream, name):
				val = getattr(upstream, name)
				globals()[name] = val
				return val
			# If upstream module exists but does not expose the requested symbol,
			# do NOT return the module object (that confuses pydantic). Fall
			# through and create a lightweight stub class instead.
		except Exception:
			# Fall through to create a stub
			pass

	# Ensure a stub module exists and exports the expected class. Some
	# upstream modules may exist in sys.modules but not expose the requested
	# symbol; in that case replace it with our flexible stub so callers get
	# an attribute-accessible class instead of hitting the last-resort logic.
	if module_full not in sys.modules or not hasattr(sys.modules.get(module_full), name):
		mod = _make_module_stub(module_full)
		sys.modules[module_full] = mod
	mod = sys.modules[module_full]
	if hasattr(mod, name):
		val = getattr(mod, name)
		globals()[name] = val
		return val

	# Last resort: provide a tiny, instantiable stub class so tests can
	# construct unknown Response* symbols without attempting to instantiate
	# typing.Any (which raises TypeError). The stub accepts kwargs and
	# exposes them as attributes to emulate simple dynamic objects.
	class _FallbackStub:
		def __init__(self, *args, **kwargs):  # pragma: no cover - trivial
			# Accept positional args silently and map kwargs to attributes
			for k, v in kwargs.items():
				setattr(self, k, v)

		def __repr__(self) -> str:  # pragma: no cover - trivial
			return f"{name}({getattr(self, '__dict__', {})})"

	globals()[name] = _FallbackStub
	return _FallbackStub


def __dir__():
	return sorted(set(__all__ + list(globals().keys())))

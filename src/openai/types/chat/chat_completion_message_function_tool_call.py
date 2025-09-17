from __future__ import annotations

from openai.types.chat._shim_base import AttrDict


class Function(AttrDict):
    pass


__all__ = ["Function"]

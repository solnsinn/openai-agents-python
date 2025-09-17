"""Stub for audio transcription create params used by third-party imports."""
from typing import TypedDict


class FileTypes(TypedDict, total=False):
    filename: str
    content_type: str


__all__ = ["FileTypes"]

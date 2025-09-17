from __future__ import annotations

from typing import TypedDict, Any


class FileFile(TypedDict, total=False):
	file_data: Any
	filename: str


class File(TypedDict, total=False):
	type: str
	file: FileFile


__all__ = ["File", "FileFile"]

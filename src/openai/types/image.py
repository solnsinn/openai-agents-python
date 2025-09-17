from typing import TypedDict, Optional


class Image(TypedDict, total=False):
    id: str
    url: str
    alt_text: Optional[str]


class ImageCreateUpload(TypedDict, total=False):
    filename: str
    data: bytes


__all__ = ["Image", "ImageCreateUpload"]

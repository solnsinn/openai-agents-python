from typing import List, Optional

try:
    from pydantic import BaseModel


    class Image(BaseModel):
        url: Optional[str] = None
        b64_json: Optional[str] = None


    class ImagesResponse(BaseModel):
        data: List[Image] = []

except Exception:
    class Image:
        def __init__(self, url: str | None = None, b64_json: str | None = None) -> None:
            self.url = url
            self.b64_json = b64_json


    class ImagesResponse:
        def __init__(self, data: list[Image] | None = None) -> None:
            self.data = data or []


__all__ = ["Image", "ImagesResponse"]

from __future__ import annotations

from typing import Optional, Any

try:
    from pydantic import BaseModel

    class UserLocation(BaseModel):
        country: Optional[str] = None
        region: Optional[str] = None
        city: Optional[str] = None

except Exception:
    class UserLocation:
        def __init__(self, country: Any = None, region: Any = None, city: Any = None):
            self.country = country
            self.region = region
            self.city = city

__all__ = ["UserLocation"]

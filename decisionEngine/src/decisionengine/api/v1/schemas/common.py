from typing import Any, Dict, Optional
from pydantic import BaseModel

class LocationSchema(BaseModel):
    id: Optional[int] = None
    lat: float
    lon: float


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None
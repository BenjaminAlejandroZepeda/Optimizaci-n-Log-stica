from typing import Any, Dict, List
from pydantic import BaseModel

from decisionengine.api.v1.schemas.common import LocationSchema


class RouteSchema(BaseModel):
    origin: LocationSchema
    destination: LocationSchema
    path: List[LocationSchema]
    distance_km: float
    estimated_travel_time_min: float
    metadata: Dict[str, Any] = {}



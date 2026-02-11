
from pydantic import BaseModel, Field

from decisionengine.api.v1.schemas.common import LocationSchema


class VehicleSchema(BaseModel):
    id: int
    type: str = Field(..., description="vehicle type, e.g. bike, van")
    capacity_kg: float
    current_location: LocationSchema
    is_available: bool = True
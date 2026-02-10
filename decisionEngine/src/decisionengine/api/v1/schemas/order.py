
from decisionEngine.src.decisionengine.api.v1.schemas.common import LocationSchema
from pydantic import BaseModel

class OrderCreateSchema(BaseModel):
    origin: LocationSchema
    destination: LocationSchema
    weight_kg: float
    priority: str
    required_vehicle_type: str
    max_wait_time_min: float
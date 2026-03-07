from pydantic import BaseModel
from typing import Optional
from decisionengine.models.enums import VehicleType, Priority


class OrderCreateSchema(BaseModel):
    weight_kg: float
    required_vehicle_type: VehicleType
    max_wait_time_seconds: float
    priority: Priority
    origin_lat: float
    origin_lng: float
    destination_lat: float
    destination_lng: float


class OrderResponseSchema(BaseModel):
    id: Optional[str]
    weight_kg: float
    required_vehicle_type: VehicleType
    priority: Priority
    origin_lat: float
    origin_lng: float
    destination_lat: float
    destination_lng: float
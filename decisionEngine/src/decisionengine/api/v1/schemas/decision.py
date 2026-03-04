from pydantic import BaseModel
from typing import Optional

from decisionengine.api.v1.schemas.vehicle import VehicleSchema
from decisionengine.api.v1.schemas.route import RouteSchema
from decisionengine.api.v1.schemas.debug import DecisionDebugInfoSchema


class DecisionResultSchema(BaseModel):
    vehicle: VehicleSchema
    route: RouteSchema
    score: float
    debug: Optional[DecisionDebugInfoSchema] = None

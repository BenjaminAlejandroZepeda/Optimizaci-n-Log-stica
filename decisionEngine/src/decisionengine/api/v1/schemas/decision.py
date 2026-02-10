from typing import List, Optional
from pydantic import BaseModel

from decisionEngine.src.decisionengine.api.v1.schemas.debug import DecisionDebugInfoSchema
from decisionEngine.src.decisionengine.api.v1.schemas.route import RouteSchema
from decisionEngine.src.decisionengine.api.v1.schemas.vehicle import VehicleSchema

class DecisionCandidateSchema(BaseModel):
    vehicle: VehicleSchema
    route: RouteSchema
    score: float
    debug: Optional[DecisionDebugInfoSchema] = None




class DecisionResultSchema(BaseModel):
    selected: DecisionCandidateSchema
    candidates: List[DecisionCandidateSchema]
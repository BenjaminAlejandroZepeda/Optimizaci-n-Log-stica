
from typing import Dict, List
from pydantic import BaseModel

class DecisionDebugInfoSchema(BaseModel):
    vehicle_id: int
    discarded: bool
    reasons: List[str]
    metrics: Dict[str, float]
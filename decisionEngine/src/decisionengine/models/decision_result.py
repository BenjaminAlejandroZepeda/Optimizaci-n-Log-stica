from dataclasses import dataclass
from decisionengine.models.vehicle import Vehicle
from decisionengine.models.route import Route

from typing import Optional
from decisionengine.models.decision_debug import DecisionDebugInfo

@dataclass(frozen=True)
class DecisionResult:
    vehicle: Vehicle
    route: Route
    score: float
    debug: Optional[DecisionDebugInfo] = None


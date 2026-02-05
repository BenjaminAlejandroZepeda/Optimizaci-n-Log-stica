from dataclasses import dataclass
from decisionengine.models.vehicle import Vehicle
from decisionengine.models.route import Route


@dataclass(frozen=True)
class DecisionResult:
    vehicle: Vehicle
    route: Route
    score: float

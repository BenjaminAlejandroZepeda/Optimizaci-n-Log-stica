from dataclasses import dataclass
from decisionengine.models.enums import Priority

# Pesos base (ajustables)
DISTANCE_WEIGHT = 1.0
TIME_WEIGHT = 0.8
WAIT_WEIGHT = 1.2


PRIORITY_MULTIPLIER = {
    Priority.LOW: 1.3,
    Priority.STANDARD: 1.0,
    Priority.HIGH: 0.7,
    Priority.CRITICAL: 0.4,
}


@dataclass(frozen=True)
class ScoringInput:
    total_distance_km: float
    total_time_min: float
    wait_time_min: float
    priority: Priority


def score_decision(input: ScoringInput) -> float:
    """
    Lower score = better decision
    """

    priority_factor = PRIORITY_MULTIPLIER[input.priority]

    score = (
        input.total_distance_km * DISTANCE_WEIGHT
        + input.total_time_min * TIME_WEIGHT
        + input.wait_time_min * WAIT_WEIGHT
    )

    return score * priority_factor

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class DecisionDebugInfo:
    vehicle_id: int
    discarded: bool
    reasons: List[str] = field(default_factory=list)

    metrics: Dict[str, Any] = field(default_factory=dict)

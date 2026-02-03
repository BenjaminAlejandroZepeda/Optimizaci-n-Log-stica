from dataclasses import dataclass
from typing import List, Optional

from decisionengine.models.location import Location


@dataclass(frozen=True)
class Route:

    origin: Location
    destination: Location

    # Secuencia de puntos (nodos) que forman la ruta
    path: List[Location]

    # Métricas
    distance_km: float
    estimated_travel_time_min: float

    # Coste abstracto (para scoring)
    cost: float

    # Información extra (peajes, zonas, debug, etc.)
    metadata: Optional[dict] = None

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from decisionengine.models.location import Location
from decisionengine.models.enums import VehicleType


@dataclass
class Vehicle:


    id: int

    # Tipo y capacidad
    vehicle_type: VehicleType
    capacity_kg: float

    # Estado actual
    current_location: Location
    is_available: bool

    # Si no está disponible, cuándo lo estará
    available_at: Optional[datetime] = None

    # Características operativas (opcionales)
    speed_kmh: Optional[float] = None

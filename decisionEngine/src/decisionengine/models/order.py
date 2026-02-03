from dataclasses import dataclass
from datetime import timedelta

from decisionengine.models.location import Location
from decisionengine.models.enums import VehicleType, Priority
    

@dataclass
class Order:

    id: int

    # Carga
    weight_kg: float

    # Restricciones
    required_vehicle_type: VehicleType
    max_wait_time: timedelta
    priority: Priority

    # Origen / destino
    origin: Location
    destination: Location


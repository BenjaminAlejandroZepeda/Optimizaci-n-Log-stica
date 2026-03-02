from enum import Enum


class VehicleType(str, Enum):
    TRUCK = "truck"
    AMBULANCE = "ambulance"
    VAN = "van"
    BIKE = "bike"
    CAR = "car"

class Priority(str, Enum):
    LOW = "low"
    STANDARD = "standard"
    HIGH = "high"
    URGENT = "critical"

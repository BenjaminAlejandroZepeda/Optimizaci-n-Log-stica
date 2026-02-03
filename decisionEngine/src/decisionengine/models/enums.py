from enum import Enum


class VehicleType(str, Enum):
    TRUCK = "truck"
    AMBULANCE = "ambulance"
    VAN = "van"
    BIKE = "bike"

class Priority(str, Enum):
    LOW = "low"
    STANDARD = "standard"
    HIGH = "high"
    CRITICAL = "critical"

from datetime import datetime, timedelta

from decisionengine.models.vehicle import Vehicle
from decisionengine.models.location import Location
from decisionengine.models.enums import VehicleType


def test_vehicle_creation_available():
    vehicle = Vehicle(
        id=1,
        vehicle_type=VehicleType.TRUCK,
        capacity_kg=2000,
        current_location=Location(-33.44, -70.65),
        is_available=True,
        speed_kmh=60.0
    )

    assert vehicle.id == 1
    assert vehicle.is_available is True
    assert vehicle.available_at is None
    assert vehicle.capacity_kg == 2000


def test_vehicle_creation_unavailable_with_available_at():
    available_time = datetime.now() + timedelta(minutes=15)

    vehicle = Vehicle(
        id=2,
        vehicle_type=VehicleType.VAN,
        capacity_kg=1500,
        current_location=Location(-33.45, -70.66),
        is_available=False,
        available_at=available_time
    )

    assert vehicle.is_available is False
    assert vehicle.available_at == available_time


def test_vehicle_location_is_value_object():
    loc = Location(-33.44, -70.65)

    vehicle = Vehicle(
        id=3,
        vehicle_type=VehicleType.TRUCK,
        capacity_kg=3000,
        current_location=loc,
        is_available=True
    )

    assert vehicle.current_location == loc

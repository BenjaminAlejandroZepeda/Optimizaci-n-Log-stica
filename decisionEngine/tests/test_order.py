from datetime import timedelta

from decisionengine.models.location import Location
from decisionengine.models.order import Order
from decisionengine.models.enums import VehicleType, Priority


def test_order_creation():
    origin = Location(-33.44, -70.65)
    destination = Location(-33.50, -70.70)

    order = Order(
        id=1,
        weight_kg=1500.0,
        required_vehicle_type=VehicleType.TRUCK,
        max_wait_time=timedelta(minutes=30),
        priority=Priority.HIGH,
        origin=origin,
        destination=destination
    )

    assert order.id == 1
    assert order.weight_kg == 1500.0
    assert order.required_vehicle_type == VehicleType.TRUCK
    assert order.max_wait_time == timedelta(minutes=30)
    assert order.priority == Priority.HIGH
    assert order.origin == origin
    assert order.destination == destination


def test_order_different_priorities():
    origin = Location(0.0, 0.0)
    destination = Location(1.0, 1.0)

    order_low = Order(
        id=2,
        weight_kg=500.0,
        required_vehicle_type=VehicleType.VAN,
        max_wait_time=timedelta(hours=1),
        priority=Priority.LOW,
        origin=origin,
        destination=destination
    )

    assert order_low.priority == Priority.LOW

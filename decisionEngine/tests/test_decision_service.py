from decisionengine.core.decision import DecisionService
from decisionengine.core.graph import Graph
from decisionengine.models.location import Location
from decisionengine.models.order import Order
from decisionengine.models.vehicle import Vehicle
from decisionengine.models.enums import VehicleType, Priority


def test_assign_order_selects_best_vehicle():
    a = Location(0, 0)
    b = Location(0, 1)
    c = Location(0, 2)

    graph = Graph()
    graph.add_edge(a, b, 5)
    graph.add_edge(b, c, 3)

    order = Order(
        id=1,
        weight_kg=5,
        required_vehicle_type=VehicleType.BIKE,
        max_wait_time=60,
        priority=Priority.STANDARD,
        origin=b,
        destination=c,
    )

    vehicle_near = Vehicle(
        id=1,
        vehicle_type=VehicleType.BIKE,
        capacity_kg=10,
        current_location=b,
        is_available=True,
    )

    vehicle_far = Vehicle(
        id=2,
        vehicle_type=VehicleType.BIKE,
        capacity_kg=10,
        current_location=a,
        is_available=True,
    )

    service = DecisionService()

    result = service.assign_order(
        order,
        [vehicle_near, vehicle_far],
        graph,
    )

    assert result.vehicle.id == 1
    assert result.route.origin == b
    assert result.route.destination == c

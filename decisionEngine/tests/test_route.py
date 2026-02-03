from decisionengine.models.location import Location
from decisionengine.models.route import Route


def test_route_creation():
    origin = Location(-33.44, -70.65)
    destination = Location(-33.45, -70.66)

    path = [
        origin,
        Location(-33.445, -70.655),
        destination
    ]

    route = Route(
        origin=origin,
        destination=destination,
        path=path,
        distance_km=12.5,
        estimated_travel_time_min=25.0,
        cost=42.0
    )

    assert route.origin == origin
    assert route.destination == destination
    assert route.path == path
    assert route.distance_km == 12.5
    assert route.estimated_travel_time_min == 25.0
    assert route.cost == 42.0
    assert route.metadata is None


def test_route_with_metadata():
    origin = Location(0.0, 0.0)
    destination = Location(1.0, 1.0)

    metadata = {
        "tolls": True,
        "zone": "urban"
    }

    route = Route(
        origin=origin,
        destination=destination,
        path=[origin, destination],
        distance_km=100.0,
        estimated_travel_time_min=120.0,
        cost=80.0,
        metadata=metadata
    )

    assert route.metadata["tolls"] is True
    assert route.metadata["zone"] == "urban"

from decisionengine.api.v1.mappers.route_mapper import RouteMapper
from decisionengine.models.route import Route
from decisionengine.models.location import Location


def test_route_to_schema():
    route = Route(
        origin=Location(latitude=0, longitude=0),
        destination=Location(latitude=1, longitude=1),
        path=[
            Location(latitude=0, longitude=0),
            Location(latitude=1, longitude=1),
        ],
        distance_km=10.5,
        estimated_travel_time_min=15,
        cost=10.5,  
        metadata={"algo": "A*"},
    )


    schema = RouteMapper.to_schema(route)

    assert schema.distance_km == 10.5
    assert schema.estimated_travel_time_min == 15
    assert schema.metadata["algo"] == "A*"
    assert len(schema.path) == 2
    assert schema.origin.lat == 0
    assert schema.destination.lon == 1

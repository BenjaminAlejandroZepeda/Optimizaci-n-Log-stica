
from decisionengine.core.graph import Graph
from decisionengine.core.decision import build_route
from decisionengine.models.location import Location


def test_build_route_metrics():
    a = Location(0, 0)
    b = Location(0, 1)
    c = Location(0, 2)

    graph = Graph()
    graph.add_edge(a, b, 5)
    graph.add_edge(b, c, 3)

    route = build_route([a, b, c], graph, speed_kmh=60)

    assert route.origin == a
    assert route.destination == c
    assert route.path == [a, b, c]

    assert route.distance_km == 8

    assert route.estimated_travel_time_min == 8

    assert route.cost == 8


def test_build_route_invalid_path():
    a = Location(0, 0)
    graph = Graph()

    try:
        build_route([a], graph)
        assert False, "Expected ValueError"
    except ValueError:
        assert True

import pytest

from decisionengine.dependencies import (
    get_graph,
    get_heuristic,
    get_decision_service,
    get_vehicles,
    get_decision_context,
)
from decisionengine.core.graph import Graph
from decisionengine.core.decision import DecisionService
from decisionengine.models.vehicle import Vehicle
from decisionengine.models.location import Location


def test_get_graph_singleton():
    graph1 = get_graph()
    graph2 = get_graph()

    assert isinstance(graph1, Graph)
    assert graph1 is graph2  # singleton en memoria


def test_graph_has_expected_edges():
    graph = get_graph()

    a = Location(0, 0)
    b = Location(0, 1)
    c = Location(0, 2)

    assert graph.cost(a, b) == 5
    assert graph.cost(b, c) == 3


def test_get_heuristic():
    heuristic = get_heuristic()

    a = Location(0, 0)
    b = Location(1, 1)

    assert callable(heuristic)
    assert heuristic(a, b) == 0.0


def test_get_decision_service():
    service = get_decision_service(get_heuristic())

    assert isinstance(service, DecisionService)
    assert service.heuristic(Location(0, 0), Location(1, 1)) == 0.0


def test_get_vehicles():
    vehicles = get_vehicles()

    assert isinstance(vehicles, list)
    assert len(vehicles) == 2
    assert all(isinstance(v, Vehicle) for v in vehicles)


def test_get_decision_context():
    service, graph, vehicles = get_decision_context(
        service=get_decision_service(get_heuristic()),
        graph=get_graph(),
        vehicles=get_vehicles(),
    )

    assert isinstance(service, DecisionService)
    assert isinstance(graph, Graph)
    assert isinstance(vehicles, list)
    assert all(isinstance(v, Vehicle) for v in vehicles)

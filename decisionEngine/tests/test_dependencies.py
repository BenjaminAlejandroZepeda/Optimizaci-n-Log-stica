import pytest

from decisionengine.dependencies import (
    get_graph,
    get_heuristic,
    get_decision_service,
    get_vehicle_repository,
    get_decision_context,
)

from decisionengine.core.graph import Graph

from decisionengine.models.vehicle import Vehicle
from decisionengine.models.location import Location
from decisionengine.core.vehicle_repository import VehicleRepository
from decisionengine.db.in_memory_vehicle_repository import InMemoryVehicleRepository
from decisionengine.core.decision import DecisionService


@pytest.fixture
def repo():
    return InMemoryVehicleRepository()


@pytest.fixture
def heuristic():
    return get_heuristic()


@pytest.fixture
def service(repo, heuristic):
    return DecisionService(
        vehicle_repository=repo,
        heuristic=heuristic,
    )



def test_get_graph_singleton():
    graph1 = get_graph()
    graph2 = get_graph()

    assert isinstance(graph1, Graph)
    assert graph1 is graph2


def test_graph_has_expected_edges():
    graph = get_graph()

    a = Location(0, 0)
    b = Location(0, 1)
    c = Location(0, 2)

    assert graph.cost(a, b) == 5
    assert graph.cost(b, c) == 3


def test_get_heuristic(heuristic):
    a = Location(0, 0)
    b = Location(1, 1)

    assert callable(heuristic)
    assert heuristic(a, b) == 0.0


def test_get_decision_service(service):
    assert isinstance(service, DecisionService)


    assert service._heuristic(Location(0, 0), Location(1, 1)) == 0.0


def test_get_vehicle_repository(repo):
    assert isinstance(repo, VehicleRepository)

    vehicles = repo.get_available_vehicles()

    assert isinstance(vehicles, list)
    assert len(vehicles) == 2
    assert all(isinstance(v, Vehicle) for v in vehicles)


def test_get_decision_context(service, repo):
    graph = get_graph()

    decision_service, graph_obj, vehicle_repository = get_decision_context(
        service=service,
        graph=graph,
        vehicle_repository=repo,
    )

    assert isinstance(decision_service, DecisionService)
    assert isinstance(graph_obj, Graph)
    assert isinstance(vehicle_repository, VehicleRepository)

    vehicles = vehicle_repository.get_available_vehicles()

    assert isinstance(vehicles, list)
    assert all(isinstance(v, Vehicle) for v in vehicles)

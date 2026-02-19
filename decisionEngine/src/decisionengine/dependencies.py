from fastapi import Depends

from decisionengine.core.graph import Graph
from decisionengine.core.decision import DecisionService
from decisionengine.models.location import Location
from decisionengine.models.vehicle import Vehicle
from decisionengine.models.enums import VehicleType
from decisionengine.core.vehicle_repository import VehicleRepository
from decisionengine.db.in_memory_vehicle_repository import InMemoryVehicleRepository


_graph: Graph | None = None


def get_graph() -> Graph:
    global _graph

    if _graph is None:
        graph = Graph()

        a = Location(0, 0)
        b = Location(0, 1)
        c = Location(0, 2)
        d = Location(1, 1)

        graph.add_edge(a, b, 5)
        graph.add_edge(b, c, 3)
        graph.add_edge(a, d, 7)
        graph.add_edge(d, a, 7)

        _graph = graph

    return _graph


def zero_heuristic(a: Location, b: Location) -> float:
    return 0.0


def get_heuristic():
    return zero_heuristic


def get_vehicle_repository() -> VehicleRepository:
    return InMemoryVehicleRepository()


def get_decision_service(
    heuristic=Depends(get_heuristic),
    vehicle_repository: VehicleRepository = Depends(get_vehicle_repository),
) -> DecisionService:
    return DecisionService(
        heuristic=heuristic,
        vehicle_repository=vehicle_repository,
    )


def get_decision_context(
    service: DecisionService = Depends(get_decision_service),
    graph: Graph = Depends(get_graph),
    vehicle_repository: VehicleRepository = Depends(get_vehicle_repository),
):
    return service, graph, vehicle_repository

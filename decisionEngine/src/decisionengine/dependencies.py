from fastapi import Depends

from decisionengine.core.graph import Graph
from decisionengine.core.decision import DecisionService
from decisionengine.models.location import Location
from decisionengine.models.vehicle import Vehicle
from decisionengine.models.enums import VehicleType



_graph: Graph | None = None


def get_graph() -> Graph:
    global _graph

    if _graph is None:
        graph = Graph()

        a = Location(0, 0)
        b = Location(0, 1)
        c = Location(0, 2)

        graph.add_edge(a, b, 5)
        graph.add_edge(b, c, 3)

        _graph = graph

    return _graph




def zero_heuristic(a: Location, b: Location) -> float:
    return 0.0


def get_heuristic():
    return zero_heuristic



def get_decision_service(
    heuristic=Depends(get_heuristic),
) -> DecisionService:
    return DecisionService(heuristic=heuristic)



def get_vehicles() -> list[Vehicle]:
    return [
        Vehicle(
            id=1,
            vehicle_type=VehicleType.BIKE,
            capacity_kg=10,
            current_location=Location(0, 1),
            is_available=True,
        ),
        Vehicle(
            id=2,
            vehicle_type=VehicleType.BIKE,
            capacity_kg=10,
            current_location=Location(0, 0),
            is_available=True,
        ),
    ]



def get_decision_context(
    service: DecisionService = Depends(get_decision_service),
    graph: Graph = Depends(get_graph),
    vehicles: list[Vehicle] = Depends(get_vehicles),
) -> tuple[DecisionService, Graph, list[Vehicle]]:
    return service, graph, vehicles

from typing import Callable, List

from decisionengine.core.astar import astar
from decisionengine.core.graph import Graph
from decisionengine.models.order import Order
from decisionengine.models.vehicle import Vehicle
from decisionengine.models.route import Route
from decisionengine.models.location import Location
from decisionengine.models.decision_result import DecisionResult

DEFAULT_SPEED_KMH = 40.0  # velocidad urbana promedio


def build_route(
    path: list[Location],
    graph: Graph,
    speed_kmh: float = DEFAULT_SPEED_KMH,
) -> Route:
    if len(path) < 2:
        raise ValueError("Route path must contain at least two locations")

    total_distance = 0.0

    for i in range(len(path) - 1):
        total_distance += graph.cost(path[i], path[i + 1])

    travel_time_min = (total_distance / speed_kmh) * 60

    return Route(
        origin=path[0],
        destination=path[-1],
        path=path,
        distance_km=total_distance,
        estimated_travel_time_min=travel_time_min,
        cost=total_distance,
        metadata={
            "speed_kmh": speed_kmh,
            "edges": len(path) - 1,
        },
    )



def default_heuristic(a: Location, b: Location) -> float:
    return 0.0


class DecisionService:

    def __init__(
        self,
        heuristic: Callable[[Location, Location], float] = default_heuristic,
    ):
        self.heuristic = heuristic

    def assign_order(
        self,
        order: Order,
        vehicles: List[Vehicle],
        graph: Graph,
    ) -> DecisionResult:

        candidates: List[DecisionResult] = []

        for vehicle in vehicles:
            if not vehicle.is_available:
                continue

            if vehicle.capacity_kg < order.weight_kg:
                continue

            if vehicle.vehicle_type != order.required_vehicle_type:
                continue

            

            # Ruta: vehículo → origen pedido
            if vehicle.current_location == order.origin:
                route_to_origin = None
                access_distance = 0.0
                access_time = 0.0
                path_to_origin = [order.origin]
            else:
                path_to_origin = astar(
                    graph,
                    vehicle.current_location,
                    order.origin,
                    self.heuristic,
                )

                route_to_origin = build_route(path_to_origin, graph)
                access_distance = route_to_origin.distance_km
                access_time = route_to_origin.estimated_travel_time_min



            # Ruta: origen → destino pedido
            path_delivery = astar(
                graph,
                order.origin,
                order.destination,
                self.heuristic,
            )

            delivery_route = build_route(path_delivery, graph)

            total_distance = access_distance + delivery_route.distance_km

            estimated_travel_time_min = (
            access_time + delivery_route.estimated_travel_time_min
            )

            full_path = (
                path_to_origin
                if route_to_origin is None
                else route_to_origin.path
            )

            full_path = full_path + delivery_route.path[1:]


            score = total_distance  # scoring simple inicial

            full_route = Route(
                origin=vehicle.current_location,
                destination=order.destination,
                path=full_path,
                distance_km=total_distance,
                estimated_travel_time_min=estimated_travel_time_min,
                cost=total_distance,
                metadata={
                    "vehicle_id": vehicle.id,
                },
            )


            candidates.append(
                DecisionResult(
                    vehicle=vehicle,
                    route=full_route,
                    score=score,
                )
            )

        if not candidates:
            raise ValueError("No suitable vehicle found for order")

        return min(candidates, key=lambda r: r.score)
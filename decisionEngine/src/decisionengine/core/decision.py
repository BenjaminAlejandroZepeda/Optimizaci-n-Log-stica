from __future__ import annotations
from typing import Callable, List

from decisionengine.core.astar import astar
from decisionengine.core.graph import Graph
from decisionengine.core.vehicle_repository import VehicleRepository
from decisionengine.models.order import Order
from decisionengine.models.vehicle import Vehicle
from decisionengine.models.route import Route
from decisionengine.models.location import Location
from decisionengine.models.decision_result import DecisionResult
from decisionengine.models.decision_debug import DecisionDebugInfo
from decisionengine.core.scoring import ScoringInput, score_decision
from decisionengine.core.exceptions import (
    NoVehicleAvailableError,
    RouteNotFoundError,
)

DEFAULT_SPEED_KMH = 40.0


def build_route(
    path: list[Location],
    graph: Graph,
    speed_kmh: float = DEFAULT_SPEED_KMH,
) -> Route:


    if not path or len(path) < 2:
        raise ValueError("Route path must contain at least two locations")

    total_distance = sum(
        graph.cost(path[i], path[i + 1])
        for i in range(len(path) - 1)
    )

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


class DecisionService:

    def __init__(
        self,
        vehicle_repository: VehicleRepository | None = None,
        heuristic: Callable | None = None,
    ):
        self._vehicle_repository = vehicle_repository
        self._heuristic = heuristic or (lambda a, b: 0.0)

    def assign_order(
        self,
        order: Order,
        graph: Graph,
        vehicles: list[Vehicle] | None = None,
    ) -> DecisionResult:

        candidates = self._evaluate_candidates(order, graph, vehicles)

        if not candidates:
            raise NoVehicleAvailableError(
                "No suitable vehicle found for the order"
            )

        best = min(candidates, key=lambda d: d.score)

        if self._vehicle_repository is not None:
            best.vehicle.is_available = False
            self._vehicle_repository.update(best.vehicle)

        return best


    def preview_order_decision(
        self,
        order: Order,
        graph: Graph,
        vehicles: list[Vehicle] | None = None,
    ) -> list[DecisionResult]:

        results = self._evaluate_candidates(order, graph, vehicles)
        return sorted(results, key=lambda d: d.score)

 
    def _evaluate_candidates(
        self,
        order: Order,
        graph: Graph,
        vehicles: list[Vehicle] | None = None,
    ) -> List[DecisionResult]:

        if vehicles is None:
            if not self._vehicle_repository:
                raise ValueError("Vehicle repository not configured")
            vehicles = self._vehicle_repository.list_available()

        results: List[DecisionResult] = []

        for vehicle in vehicles:

            if not self._is_vehicle_eligible(vehicle, order):
                continue

            decision = self._evaluate_vehicle(vehicle, order, graph)

            if decision:
                results.append(decision)

        return results

    def _is_vehicle_eligible(self, vehicle: Vehicle, order: Order) -> bool:
        return (
            vehicle.vehicle_type == order.required_vehicle_type
            and vehicle.capacity_kg >= order.weight_kg
        )

    def _evaluate_vehicle(
        self,
        vehicle: Vehicle,
        order: Order,
        graph: Graph,
    ) -> DecisionResult | None:

        debug = DecisionDebugInfo(
            vehicle_id=vehicle.id,
            discarded=False,
            reasons=[],
            metrics={},
        )


        access_path = self._calculate_path(
            graph,
            vehicle.current_location,
            order.origin,
        )

        access_route = (
            None
            if len(access_path) < 2
            else build_route(access_path, graph)
        )

        access_distance = access_route.distance_km if access_route else 0.0
        access_time = (
            access_route.estimated_travel_time_min
            if access_route else 0.0
        )

        max_wait_min = order.max_wait_time.total_seconds() / 60

        if access_time > max_wait_min:
            return None


        delivery_path = self._calculate_path(
            graph,
            order.origin,
            order.destination,
        )

        delivery_route = build_route(delivery_path, graph)

        total_distance = access_distance + delivery_route.distance_km
        total_time = access_time + delivery_route.estimated_travel_time_min

        scoring_input = ScoringInput(
            total_distance_km=total_distance,
            total_time_min=total_time,
            wait_time_min=access_time,
            priority=order.priority,
        )

        score = score_decision(scoring_input)

        full_path = (
            access_path + delivery_route.path[1:]
            if access_path
            else delivery_route.path
        )

        route = Route(
            origin=vehicle.current_location,
            destination=order.destination,
            path=full_path,
            distance_km=total_distance,
            estimated_travel_time_min=total_time,
            cost=total_distance,
            metadata={"vehicle_id": vehicle.id},
        )

        debug.metrics.update({
            "total_distance_km": total_distance,
            "total_time_min": total_time,
            "score": score,
        })

        return DecisionResult(
            vehicle=vehicle,
            route=route,
            score=score,
            debug=debug,
        )

    def _calculate_path(
        self,
        graph: Graph,
        origin: Location,
        destination: Location,
    ) -> list[Location]:

        path = astar(
            graph,
            origin,
            destination,
            self._heuristic,
        )

        if not path:
            raise RouteNotFoundError(
                f"No route found from {origin} to {destination}"
            )

        return path
from decisionengine.api.v1.mappers.decision_mapper import DecisionMapper
from decisionengine.models.decision_result import DecisionResult
from decisionengine.models.decision_debug import DecisionDebugInfo
from decisionengine.models.vehicle import Vehicle
from decisionengine.models.route import Route
from decisionengine.models.location import Location
from decisionengine.models.enums import VehicleType


def build_decision(debug: bool):
    vehicle = Vehicle(
        id=1,
        vehicle_type=VehicleType.VAN,
        capacity_kg=100,
        current_location=Location(latitude=0, longitude=0),
        is_available=True,
    )

    route = Route(
        origin=Location(latitude=0, longitude=0),
        destination=Location(latitude=1, longitude=1),
        path=[],
        distance_km=5,
        estimated_travel_time_min=10,
        metadata={},
    )

    debug_info = (
        DecisionDebugInfo(
            vehicle_id=1,
            discarded=False,
            reasons=[],
            metrics={"score": 0.9},
        )
        if debug
        else None
    )

    return DecisionResult(
        vehicle=vehicle,
        route=route,
        score=0.9,
        debug=debug_info,
    )

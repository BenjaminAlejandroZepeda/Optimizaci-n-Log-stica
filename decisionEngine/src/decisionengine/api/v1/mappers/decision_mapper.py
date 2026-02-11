from decisionengine.models.decision_result import DecisionResult
from decisionengine.api.v1.schemas.decision import (
    DecisionResultSchema,
    DecisionCandidateSchema,
)
from decisionengine.api.v1.schemas.debug import DecisionDebugInfoSchema
from .vehicle_mapper import VehicleMapper
from .route_mapper import RouteMapper


class DecisionMapper:

    @staticmethod
    def to_schema(
        decision: DecisionResult,
        *,
        debug: bool = False,
    ) -> DecisionResultSchema:

        candidate = DecisionCandidateSchema(
            vehicle=VehicleMapper.to_schema(decision.vehicle),
            route=RouteMapper.to_schema(decision.route),
            score=decision.score,
            debug=(
                DecisionDebugInfoSchema(
                    vehicle_id=decision.debug.vehicle_id,
                    discarded=decision.debug.discarded,
                    reasons=decision.debug.reasons,
                    metrics=decision.debug.metrics,
                )
                if debug and decision.debug
                else None
            ),
        )

        return DecisionResultSchema(
            selected=candidate,
            candidates=[],  
        )

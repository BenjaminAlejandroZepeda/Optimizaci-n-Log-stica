from fastapi import APIRouter, Depends

from decisionengine.api.v1.schemas.order import OrderCreateSchema
from decisionengine.api.v1.schemas.scoring import ScoringExplainSchema, ScoringFactorSchema
from decisionengine.api.v1.mappers.order_mapper import OrderMapper
from decisionengine.core.scoring import (
    ScoringInput,
    score_decision,
    DISTANCE_WEIGHT,
    TIME_WEIGHT,
    WAIT_WEIGHT,
    PRIORITY_MULTIPLIER,
)
from decisionengine.dependencies import get_current_user

router = APIRouter(
    prefix="/scoring",
    tags=["scoring"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/explain", response_model=ScoringExplainSchema)
def explain_scoring(order: OrderCreateSchema):
    """
    Devuelve el desglose del score para una orden dada,
    mostrando la contribución de cada factor (distancia, tiempo, espera)
    y el multiplicador de prioridad.
    Útil para entender por qué un vehículo fue elegido sobre otro.
    """
    domain_order = OrderMapper.from_schema(order)

    # Usamos valores de ejemplo para ilustrar el desglose
    # En la práctica esto se llama con los valores reales de un DecisionResult
    example_input = ScoringInput(
        total_distance_km=0.0,
        total_time_min=0.0,
        wait_time_min=0.0,
        priority=domain_order.priority,
    )

    priority_multiplier = PRIORITY_MULTIPLIER[domain_order.priority]

    distance_contrib = example_input.total_distance_km * DISTANCE_WEIGHT
    time_contrib = example_input.total_time_min * TIME_WEIGHT
    wait_contrib = example_input.wait_time_min * WAIT_WEIGHT
    raw_score = distance_contrib + time_contrib + wait_contrib
    total_score = raw_score * priority_multiplier

    return ScoringExplainSchema(
        total_score=total_score,
        priority_multiplier=priority_multiplier,
        raw_score=raw_score,
        factors=[
            ScoringFactorSchema(
                name="distance",
                value=example_input.total_distance_km,
                weight=DISTANCE_WEIGHT,
                contribution=distance_contrib,
                description="Distancia total recorrida en km (vehículo → origen → destino)",
            ),
            ScoringFactorSchema(
                name="time",
                value=example_input.total_time_min,
                weight=TIME_WEIGHT,
                contribution=time_contrib,
                description="Tiempo total estimado de viaje en minutos",
            ),
            ScoringFactorSchema(
                name="wait",
                value=example_input.wait_time_min,
                weight=WAIT_WEIGHT,
                contribution=wait_contrib,
                description="Tiempo de espera del vehículo hasta llegar al origen",
            ),
        ],
    )


@router.get("/weights")
def get_scoring_weights():
    """
    Devuelve los pesos y multiplicadores de prioridad actuales del sistema de scoring.
    """
    return {
        "weights": {
            "distance": DISTANCE_WEIGHT,
            "time": TIME_WEIGHT,
            "wait": WAIT_WEIGHT,
        },
        "priority_multipliers": {
            priority.value: multiplier
            for priority, multiplier in PRIORITY_MULTIPLIER.items()
        },
        "note": "Lower score = better decision",
    }
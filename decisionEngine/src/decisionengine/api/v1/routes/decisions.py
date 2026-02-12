from fastapi import APIRouter, Depends, Query, HTTPException, status

from decisionengine.api.v1.schemas.order import OrderCreateSchema
from decisionengine.api.v1.schemas.decision import DecisionResultSchema
from decisionengine.api.v1.schemas.common import ErrorResponse
from decisionengine.dependencies import get_decision_context
from decisionengine.api.v1.mappers.order_mapper import OrderMapper
from decisionengine.api.v1.mappers.decision_mapper import DecisionMapper

router = APIRouter(prefix="/decisions", tags=["decisions"])


@router.post(
    "/assign",
    response_model=DecisionResultSchema,
    responses={400: {"model": ErrorResponse}},
)
def assign_decision(
    order: OrderCreateSchema,
    debug: bool = Query(False),
    context=Depends(get_decision_context),
):
    service, graph, vehicles = context

    try:
        domain_order = OrderMapper.from_schema(order)

        decision = service.assign_order(
            order=domain_order,
            vehicles=vehicles,
            graph=graph,
        )

        if decision is None:
            raise ValueError("No available vehicle found")

        return DecisionMapper.to_schema(decision, debug=debug)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/preview",
    response_model=list[DecisionResultSchema],
    responses={400: {"model": ErrorResponse}},
)
def preview_decision(
    order: OrderCreateSchema,
    debug: bool = Query(False),
    context=Depends(get_decision_context),
):
    service, graph, vehicles = context

    try:
        domain_order = OrderMapper.from_schema(order)

        decisions = service.preview_order_decision(
            order=domain_order,
            vehicles=vehicles,
            graph=graph,
        )

        return [
            DecisionMapper.to_schema(d, debug=debug)
            for d in decisions
        ]

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

from fastapi import APIRouter, Depends, HTTPException, status

from decisionengine.api.v1.schemas.order import OrderCreateSchema
from decisionengine.api.v1.schemas.common import ErrorResponse
from decisionengine.api.v1.dependencies import get_decision_context
from decisionengine.api.v1.mappers.order_mapper import OrderMapper

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post(
    "/validate",
    status_code=status.HTTP_200_OK,
    responses={400: {"model": ErrorResponse}},
)
def validate_order(
    order: OrderCreateSchema,
    context=Depends(get_decision_context),
):
    service, graph, _ = context

    try:
        domain_order = OrderMapper.from_schema(order)

        # Asumimos validación implícita vía dominio
        service.assign_order(
            order=domain_order,
            vehicles=[],
            graph=graph,
        )

        return {"status": "ok"}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

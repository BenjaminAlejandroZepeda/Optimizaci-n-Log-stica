from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from decisionengine.api.v1.schemas.order import OrderCreateSchema, OrderResponseSchema
from decisionengine.api.v1.schemas.common import ErrorResponse
from decisionengine.dependencies import get_current_user, get_decision_context, get_order_repository
from decisionengine.api.v1.mappers.order_mapper import OrderMapper
from decisionengine.core.order_repository import OrderRepository

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


@router.get(
    "/",
    response_model=List[OrderResponseSchema],
    dependencies=[Depends(get_current_user)],
)
def list_orders(
    order_repository: OrderRepository = Depends(get_order_repository),
):
    """
    Historial de todas las órdenes persistidas.
    """
    orders = order_repository.list_all()
    return [OrderMapper.to_schema(o) for o in orders]


@router.get(
    "/{order_id}",
    response_model=OrderResponseSchema,
    dependencies=[Depends(get_current_user)],
    responses={404: {"model": ErrorResponse}},
)
def get_order(
    order_id: str,
    order_repository: OrderRepository = Depends(get_order_repository),
):
    """
    Obtiene una orden por su ID.
    """
    order = order_repository.get_by_id(order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found",
        )

    return OrderMapper.to_schema(order)


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
    responses={404: {"model": ErrorResponse}},
)
def delete_order(
    order_id: str,
    order_repository: OrderRepository = Depends(get_order_repository),
):
    """
    Elimina una orden por su ID.
    """
    order = order_repository.get_by_id(order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found",
        )

    order_repository.delete(order_id)
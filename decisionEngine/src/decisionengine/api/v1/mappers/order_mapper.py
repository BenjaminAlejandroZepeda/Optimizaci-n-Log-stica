from datetime import timedelta
from fastapi import HTTPException
from decisionengine.api.v1.schemas.order import OrderCreateSchema
from decisionengine.models.order import Order
from decisionengine.models.enums import VehicleType, Priority

from .location_mapper import LocationMapper


class OrderMapper:

    @staticmethod
    def from_schema(schema: OrderCreateSchema) -> Order:
        try:
            vehicle_type = VehicleType[schema.required_vehicle_type]
        except KeyError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid vehicle type: {schema.required_vehicle_type}",
            )

        try:
            priority = Priority[schema.priority]
        except KeyError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid priority: {schema.priority}",
            )

        return Order(
            id=0,
            weight_kg=schema.weight_kg,
            required_vehicle_type=vehicle_type,
            max_wait_time=timedelta(minutes=schema.max_wait_time_min),
            priority=priority,
            origin=LocationMapper.from_schema(schema.origin),
            destination=LocationMapper.from_schema(schema.destination),
        )

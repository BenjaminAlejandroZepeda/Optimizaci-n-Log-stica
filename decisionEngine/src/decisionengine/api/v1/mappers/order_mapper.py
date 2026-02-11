from decisionengine.api.v1.schemas.order import OrderCreateSchema
from decisionengine.models.order import Order
from decisionengine.models.enums import VehicleType, Priority
from datetime import timedelta
from .location_mapper import LocationMapper


class OrderMapper:

    @staticmethod
    def from_schema(schema: OrderCreateSchema) -> Order:
        return Order(
            id=0,
            weight_kg=schema.weight_kg,
            required_vehicle_type=VehicleType[schema.required_vehicle_type],
            max_wait_time=timedelta(minutes=schema.max_wait_time_min),
            priority=Priority[schema.priority],
            origin=LocationMapper.from_schema(schema.origin),
            destination=LocationMapper.from_schema(schema.destination),
        )

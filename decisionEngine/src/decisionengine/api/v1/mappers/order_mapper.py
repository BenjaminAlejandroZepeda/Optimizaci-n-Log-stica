from datetime import timedelta
from decisionengine.api.v1.schemas.order import OrderCreateSchema, OrderResponseSchema
from decisionengine.models.order import Order
from decisionengine.models.enums import VehicleType, Priority
from decisionengine.models.location import Location


class OrderMapper:

    @staticmethod
    def to_schema(order: Order) -> OrderResponseSchema:
        return OrderResponseSchema(
            id=order.id,
            weight_kg=order.weight_kg,
            required_vehicle_type=order.required_vehicle_type,
            priority=order.priority,
            origin_lat=order.origin.latitude,
            origin_lng=order.origin.longitude,
            destination_lat=order.destination.latitude,
            destination_lng=order.destination.longitude,
        )

    @staticmethod
    def from_schema(schema: OrderCreateSchema) -> Order:
        return Order(
            id=None,
            weight_kg=schema.weight_kg,
            required_vehicle_type=VehicleType(schema.required_vehicle_type),   
            max_wait_time=timedelta(seconds=schema.max_wait_time_seconds),      
            priority=Priority(schema.priority),                                 
            origin=Location(
                latitude=schema.origin_lat,                                     
                longitude=schema.origin_lng,
            ),
            destination=Location(
                latitude=schema.destination_lat,
                longitude=schema.destination_lng,
            ),
        )
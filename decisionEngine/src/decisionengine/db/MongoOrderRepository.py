from pymongo import MongoClient
from datetime import datetime
from decisionengine.models.order import Order
from decisionengine.models.location import Location
from decisionengine.models.enums import VehicleType

class MongoOrderRepository:

    def __init__(self, mongo_uri: str):
        self.client = MongoClient(mongo_uri)
        self.db = self.client["decision_engine"]
        self.collection = self.db["orders"]

    def save(self, order: Order) -> str:

        doc = {
            "weight_kg": order.weight_kg,
            "required_vehicle_type": order.required_vehicle_type.value,
            "max_wait_time_seconds": order.max_wait_time.total_seconds(),
            "priority": order.priority.value,
            "origin": {
                "latitude": order.origin.latitude,
                "longitude": order.origin.longitude,
            },
            "destination": {
                "latitude": order.destination.latitude,
                "longitude": order.destination.longitude,
            },
            "created_at": datetime.utcnow(),
            "status": "ASSIGNED",
        }

        result = self.collection.insert_one(doc)
        return str(result.inserted_id)
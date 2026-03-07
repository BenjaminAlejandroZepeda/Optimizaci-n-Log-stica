from pymongo import MongoClient
from datetime import datetime
from decisionengine.models.order import Order
from decisionengine.models.location import Location
from decisionengine.models.enums import VehicleType
from decisionengine.models.enums import Priority

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
    



    def get_by_id(self, order_id: str) -> Order | None:
        from bson import ObjectId
        doc = self.collection.find_one({"_id": ObjectId(order_id)})
        if not doc:
            return None
        return self._doc_to_order(doc)

    def list_all(self) -> list[Order]:
        return [self._doc_to_order(doc) for doc in self.collection.find()]

    def delete(self, order_id: str) -> None:
        from bson import ObjectId
        self.collection.delete_one({"_id": ObjectId(order_id)})

    def _doc_to_order(self, doc) -> Order:
        from datetime import timedelta
        return Order(
            id=str(doc["_id"]),
            weight_kg=doc["weight_kg"],
            required_vehicle_type=VehicleType(doc["required_vehicle_type"]),
            max_wait_time=timedelta(seconds=doc["max_wait_time_seconds"]),
            priority=Priority(doc["priority"]),
            origin=Location(doc["origin"]["latitude"], doc["origin"]["longitude"]),
            destination=Location(doc["destination"]["latitude"], doc["destination"]["longitude"]),
        )
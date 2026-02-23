from pymongo import MongoClient
from decisionengine.core.vehicle_repository import VehicleRepository
from decisionengine.models.vehicle import Vehicle
from decisionengine.models.enums import VehicleType
from decisionengine.models.location import Location


class MongoVehicleRepository(VehicleRepository):

    def __init__(self, mongo_uri: str):
        self.client = MongoClient(mongo_uri)
        self.db = self.client["decision_engine"]
        self.collection = self.db["vehicles"]

    def list_all(self) -> list[Vehicle]:
        documents = self.collection.find()
        return [self._map_to_domain(doc) for doc in documents]

    def list_available(self) -> list[Vehicle]:
        documents = self.collection.find({"is_available": True})
        return [self._map_to_domain(doc) for doc in documents]

    def get_by_id(self, vehicle_id: int) -> Vehicle | None:
        doc = self.collection.find_one({"id": vehicle_id})
        return self._map_to_domain(doc) if doc else None

    def save(self, vehicle: Vehicle) -> None:
        self.collection.insert_one(self._map_to_document(vehicle))

    def update(self, vehicle: Vehicle) -> None:
        self.collection.update_one(
            {"id": vehicle.id},
            {"$set": self._map_to_document(vehicle)},
        )

    def delete(self, vehicle_id: int) -> None:
        self.collection.delete_one({"id": vehicle_id})

    def _map_to_document(self, vehicle: Vehicle) -> dict:
        return {
            "id": vehicle.id,
            "vehicle_type": vehicle.vehicle_type.value,
            "capacity_kg": vehicle.capacity_kg,
            "current_location": {
                "latitude": vehicle.current_location.latitude,
                "longitude": vehicle.current_location.longitude,
            },
            "is_available": vehicle.is_available,
            "available_at": vehicle.available_at,
            "speed_kmh": vehicle.speed_kmh,
        }

    def _map_to_domain(self, doc: dict) -> Vehicle:
        return Vehicle(
            id=doc["id"],
            vehicle_type=VehicleType(doc["vehicle_type"]),
            capacity_kg=doc["capacity_kg"],
            current_location=Location(
                latitude=doc["current_location"]["latitude"],
                longitude=doc["current_location"]["longitude"],
            ),
            is_available=doc["is_available"],
            available_at=doc.get("available_at"),
            speed_kmh=doc.get("speed_kmh"),
        )
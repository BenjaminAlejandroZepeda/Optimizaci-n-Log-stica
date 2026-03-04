from decisionengine.core.vehicle_repository import VehicleRepository
from decisionengine.models.vehicle import Vehicle
from decisionengine.models.location import Location
from decisionengine.models.enums import VehicleType


class InMemoryVehicleRepository(VehicleRepository):

    def __init__(self, initial_vehicles: list[Vehicle] | None = None):
        if initial_vehicles is not None:
            self._vehicles: dict[int, Vehicle] = {
                v.id: v for v in initial_vehicles
            }
        else:
            # Default vehicles para tests y app
            self._vehicles: dict[int, Vehicle] = {
                1: Vehicle(
                    id=1,
                    vehicle_type=VehicleType.BIKE,
                    capacity_kg=20,
                    current_location=Location(0, 0),
                    is_available=True,
                ),
                2: Vehicle(
                    id=2,
                    vehicle_type=VehicleType.BIKE,
                    capacity_kg=10,
                    current_location=Location(0, 1),
                    is_available=True,
                ),
            }


    def get_available_vehicles(self) -> list[Vehicle]:
        return [
            v for v in self._vehicles.values()
            if v.is_available
        ]


    def list_all(self) -> list[Vehicle]:
        return list(self._vehicles.values())

    def get_by_id(self, vehicle_id: int) -> Vehicle | None:
        return self._vehicles.get(vehicle_id)

    def save(self, vehicle: Vehicle) -> None:
        self._vehicles[vehicle.id] = vehicle

    def update(self, vehicle: Vehicle) -> None:
        if vehicle.id not in self._vehicles:
            raise ValueError(f"Vehicle {vehicle.id} does not exist.")
        self._vehicles[vehicle.id] = vehicle

    def delete(self, vehicle_id: int) -> None:
        self._vehicles.pop(vehicle_id, None)

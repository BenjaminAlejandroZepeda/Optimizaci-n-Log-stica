from decisionengine.api.v1.schemas.vehicle import VehicleSchema
from decisionengine.models.vehicle import Vehicle
from .location_mapper import LocationMapper


class VehicleMapper:

    @staticmethod
    def to_schema(vehicle: Vehicle) -> VehicleSchema:
        return VehicleSchema(
            id=vehicle.id,
            type=vehicle.vehicle_type.name, 
            capacity_kg=vehicle.capacity_kg,
            current_location=LocationMapper.to_schema(vehicle.current_location),
            is_available=vehicle.is_available,
        )

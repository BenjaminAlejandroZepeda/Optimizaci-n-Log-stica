from decisionengine.api.v1.mappers.vehicle_mapper import VehicleMapper
from decisionengine.models.vehicle import Vehicle
from decisionengine.models.enums import VehicleType
from decisionengine.models.location import Location


def test_vehicle_to_schema():
    vehicle = Vehicle(
        id=1,
        vehicle_type=VehicleType.BIKE,
        capacity_kg=50,
        current_location=Location(latitude=0.0, longitude=0.0),
        is_available=True,
    )

    schema = VehicleMapper.to_schema(vehicle)

    assert schema.id == 1
    assert schema.type == "BIKE"
    assert schema.capacity_kg == 50
    assert schema.is_available is True
    assert schema.current_location.lat == 0.0


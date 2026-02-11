from decisionengine.api.v1.mappers.location_mapper import LocationMapper
from decisionengine.api.v1.schemas.common import LocationSchema
from decisionengine.models.location import Location


def test_location_from_schema():
    schema = LocationSchema(lat=-33.45, lon=-70.66)

    location = LocationMapper.from_schema(schema)

    assert location.latitude == -33.45
    assert location.longitude == -70.66


def test_location_to_schema():
    location = Location(latitude=10.0, longitude=20.0)

    schema = LocationMapper.to_schema(location)

    assert schema.lat == 10.0
    assert schema.lon == 20.0

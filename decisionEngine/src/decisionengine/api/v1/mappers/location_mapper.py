from decisionengine.api.v1.schemas.common import LocationSchema
from decisionengine.models.location import Location


class LocationMapper:

    @staticmethod
    def to_schema(location: Location) -> LocationSchema:
        return LocationSchema(
            lat=location.latitude,
            lon=location.longitude,
        )

    @staticmethod
    def from_schema(schema: LocationSchema) -> Location:
        return Location(
            latitude=schema.lat,
            longitude=schema.lon,
        )

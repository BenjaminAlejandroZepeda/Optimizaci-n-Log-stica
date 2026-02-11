from decisionengine.api.v1.schemas.route import RouteSchema
from decisionengine.models.route import Route
from .location_mapper import LocationMapper


class RouteMapper:

    @staticmethod
    def to_schema(route: Route) -> RouteSchema:
        return RouteSchema(
            origin=LocationMapper.to_schema(route.origin),
            destination=LocationMapper.to_schema(route.destination),
            path=[LocationMapper.to_schema(p) for p in route.path],
            distance_km=route.distance_km,
            estimated_travel_time_min=route.estimated_travel_time_min,
            metadata=route.metadata,
        )

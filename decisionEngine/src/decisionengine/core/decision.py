

from decisionengine.core.graph import Graph
from decisionengine.models.location import Location
from decisionengine.models.route import Route


DEFAULT_SPEED_KMH = 40.0  # velocidad urbana promedio


def build_route(
    path: list[Location],
    graph: Graph,
    speed_kmh: float = DEFAULT_SPEED_KMH,
) -> Route:
    if len(path) < 2:
        raise ValueError("Route path must contain at least two locations")

    total_distance = 0.0

    for i in range(len(path) - 1):
        total_distance += graph.cost(path[i], path[i + 1])

    travel_time_min = (total_distance / speed_kmh) * 60

    return Route(
        origin=path[0],
        destination=path[-1],
        path=path,
        distance_km=total_distance,
        estimated_travel_time_min=travel_time_min,
        cost=total_distance,
        metadata={
            "speed_kmh": speed_kmh,
            "edges": len(path) - 1,
        },
    )

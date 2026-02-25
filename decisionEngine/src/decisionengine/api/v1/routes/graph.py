from fastapi import APIRouter, Depends, HTTPException
from typing import List
import math

from decisionengine.core.graph import Graph
from decisionengine.core.astar import astar
from decisionengine.models.location import Location
from decisionengine.dependencies import get_graph
from decisionengine.api.v1.schemas.graph import (
    LocationSchema,
    EdgeSchema,
    GraphNodeSchema,
    GraphEdgeSchema,
    GraphVisualizationSchema
)
router = APIRouter(prefix="/graph", tags=["Graph"])


def euclidean(a: Location, b: Location) -> float:
    return math.sqrt(
        (a.latitude - b.latitude) ** 2 +
        (a.longitude - b.longitude) ** 2
    )


@router.get("/nodes", response_model=List[LocationSchema])
def get_nodes(graph: Graph = Depends(get_graph)):
    nodes = graph.get_nodes()

    return [
        LocationSchema(
            latitude=node.latitude,
            longitude=node.longitude,
        )
        for node in nodes
    ]

@router.get("/edges", response_model=List[EdgeSchema])
def get_edges(graph: Graph = Depends(get_graph)):
    edges = []
    adjacency = graph.get_edges()

    for origin, destinations in adjacency.items():
        for dest, cost in destinations.items():
            edges.append(
                EdgeSchema(
                    from_node=LocationSchema(
                        latitude=origin.latitude,
                        longitude=origin.longitude,
                    ),
                    to_node=LocationSchema(
                        latitude=dest.latitude,
                        longitude=dest.longitude,
                    ),
                    cost=cost,
                )
            )

    return edges

@router.get("/shortest-path")
def shortest_path(
    origin_lat: float,
    origin_lng: float,
    dest_lat: float,
    dest_lng: float,
    graph: Graph = Depends(get_graph),
):
    origin = Location(origin_lat, origin_lng)
    destination = Location(dest_lat, dest_lng)

    try:
        path = astar(graph, origin, destination, euclidean)
    except ValueError:
        raise HTTPException(status_code=404, detail="No route found")

    total_distance = 0.0
    for i in range(len(path) - 1):
        total_distance += graph.cost(path[i], path[i + 1])

    return {
        "distance": total_distance,
        "path": [
            {
                "latitude": node.latitude,
                "longitude": node.longitude,
            }
            for node in path
        ],
    }

@router.get("/visualization", response_model=GraphVisualizationSchema)
def graph_visualization(graph: Graph = Depends(get_graph)):

    adjacency = graph.get_edges()

    nodes = []
    edges = []

    node_id_map = {}

    for node in graph.get_nodes():
        node_id = f"{node.latitude}_{node.longitude}"
        node_id_map[node] = node_id

        nodes.append(
            GraphNodeSchema(
                id=node_id,
                latitude=node.latitude,
                longitude=node.longitude,
            )
        )

    for origin, destinations in adjacency.items():
        for dest, cost in destinations.items():
            edges.append(
                GraphEdgeSchema(
                    source=node_id_map[origin],
                    target=node_id_map[dest],
                    cost=cost,
                )
            )

    return GraphVisualizationSchema(
        nodes=nodes,
        edges=edges,
    )

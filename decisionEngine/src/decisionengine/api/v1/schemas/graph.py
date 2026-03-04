from pydantic import BaseModel
from typing import List


class LocationSchema(BaseModel):
    latitude: float
    longitude: float


class EdgeSchema(BaseModel):
    from_node: LocationSchema
    to_node: LocationSchema
    cost: float


class ShortestPathResponse(BaseModel):
    distance: float
    path: List[LocationSchema]



class GraphNodeSchema(BaseModel):
    id: str
    latitude: float
    longitude: float


class GraphEdgeSchema(BaseModel):
    source: str
    target: str
    cost: float


class GraphVisualizationSchema(BaseModel):
    nodes: List[GraphNodeSchema]
    edges: List[GraphEdgeSchema]
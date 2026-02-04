from typing import Dict, List
from decisionengine.models.location import Location


class Graph:
    def __init__(self):
        # Lista de Adyacencia:
        # Location -> {Location: cost}
        self._edges: Dict[Location, Dict[Location, float]] = {}

    def add_node(self, node: Location) -> None:
        if node not in self._edges:
            self._edges[node] = {}  

    def add_edge(
        self,
        from_node: Location,
        to_node: Location,
        cost: float,
        bidirectional: bool = True,
    ) -> None:
        if cost <= 0:
            raise ValueError("el costo debe ser positivo")

        self.add_node(from_node)
        self.add_node(to_node)

        self._edges[from_node][to_node] = cost

        if bidirectional:
            self._edges[to_node][from_node] = cost

    def neighbors(self, node: Location) -> List[Location]:
        return list(self._edges.get(node, {}).keys())

    def cost(self, from_node: Location, to_node: Location) -> float:
        return self._edges[from_node][to_node]

from heapq import heappush, heappop
from typing import Callable, Dict, List, Tuple

from decisionengine.models.location import Location
from decisionengine.core.graph import Graph



def reconstruct_path(
    came_from: Dict[Location, Location],
    current: Location,
) -> List[Location]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def astar(
    graph: Graph,
    start: Location,
    goal: Location,
    heuristic: Callable[[Location, Location], float],
) -> List[Location]:

    open_set: List[Tuple[float, Location]] = []
    heappush(open_set, (0.0, start))

    came_from: Dict[Location, Location] = {}

    g_score: Dict[Location, float] = {start: 0.0}

    while open_set:
        _, current = heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in graph.neighbors(current):
            tentative_g = g_score[current] + graph.cost(current, neighbor)

            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heappush(open_set, (f_score, neighbor))

    raise ValueError("No se encontró ninguna ruta entre el inicio y el objetivo")

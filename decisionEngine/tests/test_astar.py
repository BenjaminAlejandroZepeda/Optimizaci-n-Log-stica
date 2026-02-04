from decisionengine.core.astar import astar
from decisionengine.core.graph import Graph
from decisionengine.models.location import Location


def zero_heuristic(a: Location, b: Location) -> float:
    return 0.0


def test_astar_simple_path():
    a = Location(0, 0)
    b = Location(0, 1)
    c = Location(0, 2)

    graph = Graph()
    graph.add_edge(a, b, 5)
    graph.add_edge(b, c, 3)
    graph.add_edge(a, c, 8)

    path = astar(graph, a, c, zero_heuristic)

    assert path[0] == a
    assert path[-1] == c

    total_cost = sum(
        graph.cost(path[i], path[i + 1])
        for i in range(len(path) - 1)
    )

    assert total_cost == 8


def test_astar_direct_path():
    a = Location(0, 0)
    b = Location(1, 0)

    graph = Graph()
    graph.add_edge(a, b, 4)

    path = astar(graph, a, b, zero_heuristic)

    assert path == [a, b]


def test_astar_no_path():
    a = Location(0, 0)
    b = Location(1, 0)

    graph = Graph()
    graph.add_node(a)
    graph.add_node(b)

    try:
        astar(graph, a, b, zero_heuristic)
        assert False, "Expected ValueError"
    except ValueError:
        assert True

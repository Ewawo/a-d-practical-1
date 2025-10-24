from enum import Enum
from typing import List, Tuple

class EdgeType(Enum):
    PEDESTRIAN = 0
    BUS = 1
    BOTH = 2


class Edge:
    def __init__(self, vertex1: int, vertex2: int, edge_type: EdgeType):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.edge_type = edge_type
        self.available = True

    def can_use(self, other: EdgeType) -> bool:
        return self.edge_type == EdgeType.BOTH or other == EdgeType.BOTH or self.edge_type == other


class Vertex:
    def __init__(self, vertex_id: int):
        self.vertex_id = vertex_id
        self.edges = []

    def add_edge(self, edge: Edge):
        self.edges.append(edge)


def get_input() -> List[Vertex]:
    number_of_vertices, number_of_edges = map(int, input().split())
    vertices = [Vertex(i) for i in range(number_of_vertices)]

    # add every edge to both vertices
    for _ in range(number_of_edges):
        v1, v2, edge_type_int = map(int, input().split())
        edge = Edge(v1, v2, EdgeType(edge_type_int))

        vertices[v1].add_edge(edge)
        vertices[v2].add_edge(edge)

    return vertices


def cycle_search(vertices: List[Vertex]) -> int:
    # loop over all vertices
    result = 0
    for vertex in vertices:
        # per vertex check if there are any cycles for bus and pedestrian. If so, remove the first edge that is not "both". If all are "both" remove the first edge.
        # check for pedestrian first
        result += remove_edges_from_vertex(vertex, vertices, EdgeType.PEDESTRIAN)
        result += remove_edges_from_vertex(vertex, vertices, EdgeType.BUS)

    return result


def remove_edges_from_vertex(vertex: Vertex, vertices: List[Vertex], edge_type: EdgeType) -> int:
    cycles = get_all_cycles(vertex, vertices, edge_type)
    result = 0
    for cycle in cycles:
        removed = False
        for edge in cycle:
            if edge.edge_type == EdgeType.PEDESTRIAN:
                edge.available = False
                removed = True
                break

        # apparently all edges in the cycle are "both", so we just remove the first one.
        if not removed:
            cycle[0].available = False

        # update the counter + 1 for each edge that we "throw away".
        result += 1

    return result


def get_all_cycles(start_vertex: Vertex, vertices: List[Vertex], edge_type: EdgeType) -> List[List[Edge]]:
    visited = set()
    edge_stack = []
    cycles = []

    def dfs(current: Vertex):
        visited.add(current.vertex_id)

        for edge in current.edges:
            # skip invalid edges
            if not edge.available or not edge.can_use(edge_type):
                continue

            # get neighbor
            neighbor_id = edge.vertex2 if edge.vertex1 == current.vertex_id else edge.vertex1
            neighbor = vertices[neighbor_id]

            # traverse deeper
            if neighbor.vertex_id not in visited:
                edge_stack.append(edge)
                dfs(neighbor)
                edge_stack.pop()

            # if we reach the start vertex again, it's a cycle
            elif neighbor == start_vertex and edge not in edge_stack:
                    # copy the stack and add the last edge
                    cycles.append(edge_stack[:] + [edge])

    dfs(start_vertex)
    return cycles


def main():
    vertices = get_input()

    output = cycle_search(vertices)

    print(output)

if __name__ == '__main__':
    main()

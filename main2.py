from enum import Enum
from copy import deepcopy
from typing import List, Any


class RoadType(Enum):
    WALKING = 0
    BUS = 1
    BOTH = 2


class Edge:
    def __init__(self, vertex1: int, vertex2: int, road_type: RoadType):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.road_type = road_type


def get_input() -> (int, List[Edge], List[Edge], List[Edge]):
    values = input().split()
    if len(values) > 2:
        # apparently all input is on 1 line :(
        number_of_vertices, number_of_edges = map(int, values[:2])

        edge_values = values[2:]

        walking_edges = []
        bus_edges = []
        both_edges = []

        for i in range(0, len(edge_values), 3):
            vertex1 = int(edge_values[i])
            vertex2 = int(edge_values[i + 1])
            road_type = RoadType(int(edge_values[i + 2]))
            edge = Edge(vertex1, vertex2, road_type)

            if road_type == RoadType.WALKING:
                walking_edges.append(edge)
            elif road_type == RoadType.BUS:
                bus_edges.append(edge)
            elif road_type == RoadType.BOTH:
                both_edges.append(edge)

        return number_of_vertices, walking_edges, bus_edges, both_edges
    else:
        # all input is divided between lines just like the given example package! :)
        number_of_vertices, number_of_edges = map(int, values)

        walking_edges = []
        bus_edges = []
        both_edges = []

        for _ in range(number_of_edges):
            vertex1, vertex2, road_type = map(int, input().split())
            edge = Edge(vertex1, vertex2, RoadType(road_type))

            if edge.road_type == RoadType.WALKING:
                walking_edges.append(edge)
            elif edge.road_type == RoadType.BUS:
                bus_edges.append(edge)
            elif edge.road_type == RoadType.BOTH:
                both_edges.append(edge)

        return number_of_vertices, walking_edges, bus_edges, both_edges


class SetUnion:
    def __init__(self, number_of_vertices: int) -> None:
        # each vertex is its own group.
        self.parent = list(range(number_of_vertices))
        # how many seperate vertices groups do we have. At start its the amount of vertex.
        self.number_of_groups = number_of_vertices


    def find(self, vertex: int) -> int:
        root = vertex
        # needed to go for while loop instead of recursive, because python cannot handle high recursion depth.
        while root != self.parent[root]:
            root = self.parent[root]

        return root


    def union(self, start: int, end: int) -> bool:
        parent_start = self.find(start)
        parent_end = self.find(end)
        if parent_start == parent_end:
            #same parent, so in the same group (cycle) return false.
            return False

        self.parent[parent_end] = parent_start
        self.number_of_groups -= 1

        return True


    # quick deepcopy for the inner parent array
    def __deepcopy__(self, memo: dict[int, Any]) -> "SetUnion":
        new_set_union = SetUnion.__new__(SetUnion)
        new_set_union.parent = deepcopy(self.parent, memo)
        new_set_union.number_of_groups = self.number_of_groups
        return new_set_union


def find_most_closed_roads(vertices: int, walking_edges: List[Edge], bus_edges: List[Edge], both_edges: List[Edge]) -> int:
    both_union = SetUnion(vertices)
    used_roads = 0
    amount_of_roads = len(walking_edges) + len(bus_edges) + len(both_edges)

    #check for both
    used_roads += union_find(both_union, both_edges)

    #copy current union
    walking_union = deepcopy(both_union)
    bus_union = both_union

    #check walking
    used_roads += union_find(walking_union, walking_edges)

    #check bus
    used_roads += union_find(bus_union, bus_edges)

    # if there are more than 1 group, apparently the graph is not connected. return -1
    if bus_union.number_of_groups != 1 or walking_union.number_of_groups != 1:
        return -1

    return amount_of_roads - used_roads


def union_find(union: SetUnion, edges: List[Edge]) -> int:
    used_roads = 0
    for edge in edges:
        used_road = union.union(edge.vertex1,edge.vertex2)
        if used_road:
            used_roads +=1

    return used_roads


def main():
    vertices,walking_edges,bus_edges,both_edges = get_input()
    print(find_most_closed_roads(vertices,walking_edges,bus_edges,both_edges))


if __name__ == '__main__':
    main()

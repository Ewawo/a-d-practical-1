from enum import Enum
from typing import List, Tuple

class EdgeType(Enum):
    WALKING = 0
    BUS = 1
    BOTH = 2

def get_input() -> Tuple[int, List[Tuple[int, int, EdgeType]]]:
    number_of_vertices, number_of_edges = map(int, input().split())
    edges = [(a, b, EdgeType(t)) for a, b, t in
             (map(int, input().split()) for _ in range(number_of_edges))]
    return number_of_vertices, edges
class SetUnion:
    def __init__(self, number_of_vertices):
        # each vertex is its own group.
        self.parent = list(range(number_of_vertices))
        # how many seperate vertices groups do we have. At start its the amount of vertex.
        self.number_of_groups = number_of_vertices
    def find(self, vertex):
        if vertex == self.parent[vertex]:
            return vertex
        else:
            return self.find(self.parent[vertex]) 

    def union(self, start, end):
        parent_start = self.find(start)
        parent_end = self.find(end)
        if parent_start == parent_end:
            #same parent, so in the same group return false.
            return False
        self.parent[parent_end] = parent_start
        self.number_of_groups -= 1
        return True

def find_most_closed_roads(V,E):
    walking_union = SetUnion(V)
    bus_union = SetUnion(V)
    used_roads = 0
    amount_of_roads = len(E)
    #Check for both
    for start,end,road in E:
        if(road == EdgeType.BOTH):
            used_bus = bus_union.union(start,end)
            used_walking = walking_union.union(start,end)
            if used_bus or used_walking:
                used_roads +=1
    #Check walking
    for start,end,road, in E:
        if(road == EdgeType.WALKING):
            used_walking = walking_union.union(start,end)
            if used_walking:
                used_roads +=1
    #Check bus
    for start,end,road, in E :
        if(road == EdgeType.BUS):
            used_bus = bus_union.union(start,end)
            if used_bus:
                used_roads +=1
    
    if bus_union.number_of_groups != 1 or walking_union.number_of_groups != 1:
        return -1
    return amount_of_roads - used_roads
def main():
    V,E = get_input()
    print(find_most_closed_roads(V,E))

if __name__ == '__main__':
    main()

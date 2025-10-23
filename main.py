from enum import Enum
from typing import List, Tuple

class EdgeType(Enum):
    NORMAL = 0
    SPECIAL = 1
    DANGEROUS = 2

def get_input() -> Tuple[int, List[Tuple[int, int, EdgeType]]]:
    number_of_vertices, number_of_edges = map(int, input().split())
    edges = [(a, b, EdgeType(t)) for a, b, t in
             (map(int, input().split()) for _ in range(number_of_edges))]
    return number_of_vertices, edges


def main():
    # add swallow function
    input = get_input()
    print(input)

if __name__ == '__main__':
    main()

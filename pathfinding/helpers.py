from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Tuple


TRAVERSED = (255, 0, 0)  # red
IDLE = (255, 255, 255)  # white
BLOCKED = (0, 0, 0)  # black
NEIGHBOUR = (0, 255, 0)  # green
END = (255, 255, 0)  # yellow
START = (0, 0, 255)  # blue


def pythagorean_distance(node1: Node, node2: Node):
    return ((node1.x_pos - node2.x_pos) ** 2 + (node1.y_pos - node2.y_pos) ** 2) * 0.5


@dataclass
class Node:
    x_pos: int  # x pos on grid
    y_pos: int  # y pos on grid
    g_cost: float = 0  # distance from start node
    h_cost: float = 0  # distance from end node
    f_cost: float = 0  # sum of g_cost and h_cost
    state: str = "idle"  # traversed, idle, blocked, neighbour
    isStartNode: bool = False  # is it the start node
    isEndNode: bool = False  # is it the start node
    parent: Optional[Node] = None  # node originated from

    def get_neighbours(self, row_cells: int, col_cells: int) -> List[Tuple[int, int]]:
        return [
            (self.x_pos + x, self.y_pos + y)
            for x, y in [(-1, 0), (0, 1), (1, 0), (0, 1)]
            if 0 <= self.x_pos + x < row_cells and 0 <= self.y_pos < col_cells
        ]

    def update_node_costs(self, start_node: Node, end_node: Node) -> None:
        self.g_cost += pythagorean_distance(self, start_node)
        self.h_cost += pythagorean_distance(self, end_node)
        self.f_cost += self.g_cost + self.h_cost

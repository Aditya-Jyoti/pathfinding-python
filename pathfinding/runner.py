from .helpers import *
import pygame as pg


class Pathfinder:
    def __init__(self, settings: dict) -> None:
        pg.init()
        pg.display.set_caption("Python Pathfinder")

        self.cell_size = settings["cell_size"]
        self.row_cells = settings["row_cells"]
        self.col_cells = settings["col_cells"]

        self.screen = pg.display.set_mode(
            (self.row_cells * self.cell_size, self.col_cells * self.cell_size)
        )
        self.clock = pg.time.Clock()

        self.game_board = [
            [Node(x, y) for x in range(self.row_cells)] for y in range(self.col_cells)
        ]

        self.start_node = None
        self.end_node = None
        self.open_nodes = []
        self.closed_nodes = []

    def draw_board(self) -> None:
        for row in self.game_board:
            for node in row:
                pg.draw.rect(
                    self.screen,
                    START
                    if node.isStartNode
                    else END
                    if node.isEndNode
                    else eval(node.state.upper()),
                    pg.Rect(
                        node.x_pos * self.cell_size,
                        node.y_pos * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                )

        for x_idx in range(self.row_cells + 1):
            pg.draw.rect(
                self.screen,
                (0, 0, 0),
                pg.Rect(x_idx * self.cell_size, 0, 3, self.col_cells * self.cell_size),
            )

        for y_idx in range(self.col_cells + 1):
            pg.draw.rect(
                self.screen,
                (0, 0, 0),
                pg.Rect(0, y_idx * self.cell_size, self.row_cells * self.cell_size, 3),
            )

    def solve_path(self, node: Node) -> Node:
        if node.parent is None:
            return node

        self.game_board[node.y_pos][node.x_pos].isEndNode = True
        return self.solve_path(node.parent)

    def pathfind(self) -> Optional[bool]:
        if not isinstance(self.end_node, Node):
            return
        if not isinstance(self.start_node, Node):
            return

        current_node: Node = sorted(self.open_nodes, key=lambda node: node.f_cost)[0]
        current_node.state = "traversed"
        popped = self.open_nodes.pop(self.open_nodes.index(current_node))
        self.closed_nodes.append(popped)

        if current_node == self.end_node:
            self.solve_path(current_node)
            return True

        for nbr_x, nbr_y in current_node.get_neighbours(self.row_cells, self.col_cells):
            neighbour_node = self.game_board[nbr_y][nbr_x]

            if neighbour_node.state == "blocked" or neighbour_node in self.closed_nodes:
                continue

            new_g_cost = pythagorean_distance(neighbour_node, self.start_node)
            if (
                new_g_cost < neighbour_node.g_cost
                or neighbour_node not in self.open_nodes
            ):
                new_h_cost = pythagorean_distance(neighbour_node, self.end_node)

                if new_g_cost < neighbour_node.g_cost:
                    neighbour_node.update_node_costs(new_h_cost, new_g_cost)
                else:
                    neighbour_node.update_node_costs(new_h_cost)

                neighbour_node.parent = current_node
                neighbour_node.state = "neighbour"

                if neighbour_node not in self.open_nodes:
                    self.open_nodes.append(neighbour_node)

            self.game_board[nbr_y][nbr_x] = neighbour_node

    def main(self) -> None:
        self.screen.fill((255, 255, 255))
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        ret = self.pathfind()
                        while not ret:
                            ret = self.pathfind()

                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    mouse_pos_x = mouse_pos[0] // self.cell_size
                    mouse_pos_y = mouse_pos[1] // self.cell_size

                    if pg.mouse.get_pressed()[0]:
                        if not self.start_node:
                            self.start_node = self.game_board[mouse_pos_y][mouse_pos_x]
                            self.start_node.isStartNode = True
                            self.open_nodes.append(self.start_node)

                        elif not self.end_node:
                            self.end_node = self.game_board[mouse_pos_y][mouse_pos_x]
                            self.end_node.isEndNode = True

                if event.type == pg.MOUSEMOTION:
                    if not self.start_node and not self.end_node:
                        continue

                    mouse_pos = pg.mouse.get_pos()
                    mouse_pos_x = mouse_pos[0] // self.cell_size
                    mouse_pos_y = mouse_pos[1] // self.cell_size
                    pressed = pg.mouse.get_pressed()
                    node = self.game_board[mouse_pos_y][mouse_pos_x]

                    if pressed[0]:
                        if (
                            node.state == "idle"
                            and not node.isStartNode
                            and not node.isEndNode
                        ):
                            node.state = "blocked"

                    elif pressed[2]:
                        if (
                            node.state == "blocked"
                            and not node.isStartNode
                            and not node.isEndNode
                        ):
                            node.state = "idle"

            self.draw_board()

            self.clock.tick(60)
            pg.display.update()

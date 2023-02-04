from .helpers import *
import pygame as pg
from time import sleep


class Pathfinder:
    def __init__(self, settings: dict) -> None:
        pg.init()
        pg.display.set_caption("Python Pathfinder")

        self.cell_size = settings["cell_size"]
        self.row_cells = settings["row_cells"]
        self.col_cells = settings["col_cells"]
        self.add_wait_time = settings["add_wait_time"]

        self.screen = pg.display.set_mode(
            (self.row_cells * self.cell_size, self.col_cells * self.cell_size)
        )
        self.clock = pg.time.Clock()

        self.game_board = [
            [Node(x, y) for x in range(self.row_cells)] for y in range(self.col_cells)
        ]

        self.start_node = None
        self.open_nodes = set()
        self.closed_nodes = set()
        self.visual_nodes = []
        self.end_nodes = []
        self.path_nodes = []
        self.backup_nodes = {"start": None, "end": []}

    def draw_board(self) -> None:
        for row in self.game_board:
            for node in row:
                pg.draw.rect(
                    self.screen,
                    NODE_STATES[node.state],
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

    def solve_path(self, node: Node) -> bool:

        if node.parent == self.start_node:
            return True

        self.path_nodes.append(node)
        return self.solve_path(node.parent)

    def pathfind(self) -> Optional[bool]:
        if not isinstance(self.start_node, Node):
            return

        current_node: Node = min(self.open_nodes, key=lambda node: node.f_cost)
        self.open_nodes.remove(current_node)

        current_node.state = "traversed"
        self.closed_nodes.add(current_node)

        for node in self.end_nodes:
            if current_node != node:
                continue

            self.backup_nodes["end"].append(node)
            self.end_nodes.remove(node)
            self.solve_path(current_node)

            for node in self.open_nodes:
                self.visual_nodes.append(node)
                node.renew_node()

            if len(self.end_nodes) == 0:
                for node in self.visual_nodes:
                    self.game_board[node.y_pos][node.x_pos].state = "traversed"

                for node in self.path_nodes:
                    node.state = "end"
                    self.draw_board()
                    pg.display.update()

                    if self.add_wait_time:
                        sleep(0.1)

                self.game_board[self.backup_nodes["start"].y_pos][
                    self.backup_nodes["start"].x_pos
                ].state = "start"

                for node in self.backup_nodes["end"]:
                    self.game_board[node.y_pos][node.x_pos].state = "neighbour"

                return True

            for node in self.closed_nodes:
                if node.state == "blocked":
                    continue

                self.visual_nodes.append(node)
                node.renew_node()

            current_node.renew_node()
            current_node.state = "start"
            current_node.g_cost = 0

            self.start_node = current_node
            self.open_nodes = {self.start_node}

            self.closed_nodes = set(
                filter(lambda node: node.state == "blocked", self.closed_nodes)
            )

            for node in self.end_nodes:
                node.weight = pythagorean_distance(self.start_node, node)

            return

        for nbr_x, nbr_y in current_node.get_neighbours(self.row_cells, self.col_cells):
            neighbour_node = self.game_board[nbr_y][nbr_x]

            if neighbour_node in self.closed_nodes:
                continue

            new_g_cost = current_node.g_cost + 1
            if new_g_cost < neighbour_node.g_cost:
                new_h_cost = pythagorean_distance(
                    neighbour_node, min(self.end_nodes, key=lambda node: node.weight)
                )

                neighbour_node.update_node_costs(new_h_cost, new_g_cost)
                neighbour_node.parent = current_node
                neighbour_node.state = "neighbour"

                if neighbour_node not in self.open_nodes:
                    self.open_nodes.add(neighbour_node)

            self.game_board[nbr_y][nbr_x] = neighbour_node

    def main(self) -> None:
        self.screen.fill((255, 255, 255))
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.KEYDOWN:
                    self.backup_nodes["start"] = self.start_node
                    if event.key == pg.K_SPACE:
                        for node in self.end_nodes:
                            node.weight = pythagorean_distance(self.start_node, node)

                        ret = self.pathfind()
                        while not ret:
                            ret = self.pathfind()
                            self.draw_board()
                            pg.display.update()

                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    mouse_pos_x = mouse_pos[0] // self.cell_size
                    mouse_pos_y = mouse_pos[1] // self.cell_size
                    clicked_node = self.game_board[mouse_pos_y][mouse_pos_x]

                    if pg.mouse.get_pressed()[0]:
                        if clicked_node.state == "idle" and not self.start_node:
                            clicked_node.isStartNode = True
                            clicked_node.state = "start"
                            clicked_node.g_cost = 0
                            self.open_nodes.add(clicked_node)
                            self.start_node = clicked_node

                        if self.start_node:
                            if clicked_node.state == "idle":
                                clicked_node.state = "end"
                                clicked_node.isEndingNode = True
                                self.end_nodes.append(clicked_node)

                            elif clicked_node.state == "end":
                                self.end_nodes.remove(clicked_node)
                                clicked_node.isEndingNode = False
                                clicked_node.state = "idle"

                if event.type == pg.MOUSEMOTION:
                    if not self.start_node:
                        continue

                    mouse_pos = pg.mouse.get_pos()
                    mouse_pos_x = mouse_pos[0] // self.cell_size
                    mouse_pos_y = mouse_pos[1] // self.cell_size
                    pressed = pg.mouse.get_pressed()
                    node = self.game_board[mouse_pos_y][mouse_pos_x]

                    if pressed[2]:
                        if node.state == "idle":
                            node.state = "blocked"
                            self.closed_nodes.add(node)

                    # elif pressed[2]:
                    #     if (
                    #         node.state == "blocked"
                    #         and not node.isStartNode
                    #         and not node.isEndNode
                    #     ):
                    #         node.state = "idle"
                    #         self.closed_nodes.remove(node)

            self.draw_board()
            self.clock.tick(60)
            pg.display.update()

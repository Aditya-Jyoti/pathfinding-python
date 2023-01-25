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
            [Node(x, y) for x in range(self.row_cells) for y in range(self.col_cells)]
        ]

    def draw_board(self) -> None:
        for row in self.game_board:
            for node in row:
                if node.state == "idle":
                    pg.draw.rect(
                        self.screen,
                        IDLE,
                        pg.Rect(
                            node.x_pos * self.cell_size,
                            node.y_pos * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )

                elif node.state == "traversed":
                    pg.draw.rect(
                        self.screen,
                        TRAVERSED,
                        pg.Rect(
                            node.x_pos * self.cell_size,
                            node.y_pos * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )

                elif node.state == "blocked":
                    pg.draw.rect(
                        self.screen,
                        BLOCKED,
                        pg.Rect(
                            node.x_pos * self.cell_size,
                            node.y_pos * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )

                elif node.state == "neighbour":
                    pg.draw.rect(
                        self.screen,
                        NEIGHBOUR,
                        pg.Rect(
                            node.x_pos * self.cell_size,
                            node.y_pos * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )

                if node.isStartNode:
                    pg.draw.rect(
                        self.screen,
                        START,
                        pg.Rect(
                            node.x_pos * self.cell_size,
                            node.y_pos * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )

                elif node.isEndNode:
                    pg.draw.rect(
                        self.screen,
                        END,
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

    def pathfind(self) -> None:
        self.screen.fill((255, 255, 255))
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            self.draw_board()

            self.clock.tick(60)
            pg.display.update()

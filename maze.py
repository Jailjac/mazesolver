import time

from shapes import *

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self._create_cells()

    def _create_cells(self):
        x2 = self._x1 + (self._cell_size_x * self._num_cols)
        y2 = self._y1 + (self._cell_size_y * self._num_rows)
        for x in range(self._x1, x2, self._cell_size_x):
            col = []
            for y in range(self._y1, y2, self._cell_size_y):
                col.append(Cell(x, y, x + self._cell_size_x, y + self._cell_size_y, self._win))
            self._cells.append(col)

        self._draw_cells()

    def _draw_cells(self):
        for cols in self._cells:
            for cell in cols:
                cell.draw("black")

        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)
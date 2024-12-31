import time, random

from shapes import *

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win = None, seed = None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        if seed is not None:
            self._seed = random.seed(seed)
        else: 
            self._seed = random.seed()
        self._create_cells()

    def _create_cells(self):
        if self._num_cols < 1 or self._num_rows < 1:
            return
        x2 = self._x1 + (self._cell_size_x * self._num_cols)
        y2 = self._y1 + (self._cell_size_y * self._num_rows)
        for x in range(self._x1, x2, self._cell_size_x):
            col = []
            for y in range(self._y1, y2, self._cell_size_y):
                col.append(Cell(x, y, x + self._cell_size_x, y + self._cell_size_y, self._win))
            self._cells.append(col)

        self._draw_cells()

        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _draw_cells(self):
        if self._win is None:
            return
        for cols in self._cells:
            for cell in cols:
                cell.draw()

        self._animate()

    def _draw_cell(self, cell):
        if self._win is None:
            return
        cell.draw()
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(self._cells[0][0])
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._cells[self._num_cols - 1][self._num_rows - 1])

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return
        while True:
            directions = []
            wall_dict = {
                "left" : "has_left_wall",
                "right" : "has_right_wall",
                "top" : "has_top_wall",
                "bottom" : "has_bottom_wall"
            }
            inverse_dict = {
                "left" : "has_right_wall",
                "right" : "has_left_wall",
                "top" : "has_bottom_wall",
                "bottom" : "has_top_wall"
            }
            if i > 0 and not self._cells[i - 1][j].visited:
                directions.append(("left", i - 1, j))
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                directions.append(("right", i + 1, j))
            if j > 0 and not self._cells[i][j - 1].visited:
                directions.append(("top", i, j - 1))
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                directions.append(("bottom", i, j + 1))
            
            if directions == []:
                return
            direction = random.choice(directions)
            if direction[0] in wall_dict:
                setattr(self._cells[i][j], wall_dict[direction[0]], False)
                setattr(self._cells[direction[1]][direction[2]], inverse_dict[direction[0]], False)
                self._draw_cell(self._cells[i][j])

            self._break_walls_r(direction[1], direction[2])

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        possible_walls = ("has_left_wall", "has_right_wall", "has_top_wall", "has_bottom_wall")
        wall_map = {
            "has_left_wall" : (-1, 0),
            "has_right_wall" : (1, 0),
            "has_top_wall" : (0, -1),
            "has_bottom_wall" : (0, 1)
        }
        directions = []
        for wall in possible_walls:
            if (not getattr(current_cell, wall)
                and (wall != "has_top_wall" or j != 0)
                and not self._cells[i + wall_map[wall][0]][j + wall_map[wall][1]].visited):
                directions.append(wall)

        for direction in directions:
            next_i, next_j = i + wall_map[direction][0], j + wall_map[direction][1]
            next_cell = self._cells[next_i][next_j]
            current_cell.draw_move(next_cell)
            exit_found = self._solve_r(next_i, next_j)
            if exit_found:
                return True
            current_cell.draw_move(next_cell, True)

        return False
from tkinter import Canvas

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def find_center(self, other):
        avg_x = (self.x + other.x)//2
        avg_y = (self.y + other.y)//2
        return Point(avg_x, avg_y)

class Line():
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2
        )


class Cell():
    def __init__(self, x1, y1, x2, y2, win, has_left_wall = True, has_right_wall = True, has_top_wall = True, has_bottom_wall = True):
        self._bottom_left = Point(min(x1, x2), max(y1, y2))
        self._bottom_right = Point(max(x1, x2), max(y1, y2))
        self._top_left = Point(min(x1, x2), min(y1, y2))
        self._top_right = Point(max(x1, x2), min(y1, y2))
        self._win = win
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall

    def draw(self, fill_color):
        if self.has_left_wall:
            left_wall = Line(self._bottom_left, self._top_left)
            self._win.draw_line(left_wall, fill_color)
        if self.has_right_wall:
            right_wall = Line(self._bottom_right, self._top_right)
            self._win.draw_line(right_wall, fill_color)
        if self.has_top_wall:
            top_wall = Line(self._top_left, self._top_right)
            self._win.draw_line(top_wall, fill_color)
        if self.has_bottom_wall:
            bottom_wall = Line(self._bottom_left, self._bottom_right)
            self._win.draw_line(bottom_wall, fill_color)

    def draw_move(self, to_cell, undo=False):
        self_center = self._bottom_left.find_center(self._top_right)
        to_cell_center = to_cell._bottom_left.find_center(to_cell._top_right)
        move_line = Line(self_center, to_cell_center)
        color = "gray" if undo else "red"

        self._win.draw_line(move_line, color)




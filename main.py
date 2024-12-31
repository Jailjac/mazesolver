from window import Window
from shapes import *
from maze import Maze

def main():
    win = Window(800, 600, "Test Window")

    maze = Maze(10, 10, 10, 8, 50, 50, win)
    maze.solve()
    win.wait_for_close()


if __name__ == "__main__":
    main()
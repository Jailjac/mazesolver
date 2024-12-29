from window import Window

def main():
    win = Window(800, 600, "Test Window")
    win.wait_for_close()


if __name__ == "__main__":
    main()
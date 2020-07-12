import tkinter as tk

from BallGame.direction import Direction


class Player(object):
    def __init__(self, master, width, height, x_cord, y_cord):
        self.master_canvas = master
        self.height = height
        self.width = width
        self.x = None
        self.y = None
        self.canvas_index = None
        self.player_surrounding_rectangle_coords = ()
        self.create_player(height, width, x_cord, y_cord)

    def create_player(self, height, width, x_cord, y_cord):
        frame = tk.Frame(self.master_canvas, width=width, height=height, bg='yellow')
        frame.pack()

        player_index = self.master_canvas.create_window(x_cord, y_cord, window=frame)

        self.canvas_index = player_index

        self.x = self.master_canvas.coords(self.canvas_index)[0]
        self.y = self.master_canvas.coords(self.canvas_index)[1]

    def compute_surrounding_rectangle_coords(self):
        x1, y1 = (self.x - self.width / 2), (self.y - self.height / 2)
        x2, y2 = (self.x + self.width / 2), (self.y + self.height / 2)

        self.player_surrounding_rectangle_coords = (x1, y1, x2, y2)

    def move(self, direction, move_by_pixels=10):
        print(self.x)

        x = self.x
        y = self.y
        if direction == Direction.LEFT:
            x = self.x - move_by_pixels
        elif direction == Direction.RIGHT:
            x = self.x + move_by_pixels
        elif direction == Direction.UP:
            y = self.y - 10
        elif direction == Direction.DOWN:
            y = self.y + 10

        if (x - self.width / 3) <= 0 or (x + self.width / 3) >= self.master_canvas.width:
            return

        self.x = x
        self.y = y
        self.compute_surrounding_rectangle_coords()

        self.master_canvas.coords(self.canvas_index, self.x, self.y)
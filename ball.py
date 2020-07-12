import math

from BallGame.direction import Direction


class Ball(object):
    BALL_INDEXES = []
    PIXEL_PER_MOVE = 1

    def __init__(self, parent, speed, collision_callback, *coords):
        self.parent = parent
        self.collision_callback = collision_callback

        self.speed = speed
        self.canvas_index = None
        self.dx = 0
        self.dy = 10
        self.angle_wrt_x_axis = 90

        self.direction = None

        self.create_ball(coords)

        Ball.BALL_INDEXES.append(self.canvas_index)
        print(Ball.BALL_INDEXES)

    def create_ball(self, coords):
        self.canvas_index = self.parent.create_oval(coords, fill='red')
        print("oval created")

    def move(self):
        prev_cords = self.parent.coords(self.canvas_index)[0], self.parent.coords(self.canvas_index)[1]
        self.collision_callback(self)
        # print("Di:{}".format(self.direction))
        #
        # x1,y1,x2,y2 = self.parent.coords(self.canvas_index)
        #
        # print("BEFORE {},{},{},{}".format(x1,y1,x2,y2))
        #
        # if self.direction == Direction.UP:
        #     y1 -= 10
        # if self.direction == Direction.DOWN:
        #     y1 += 10
        # if self.angle_wrt_x_axis:
        #     x1 = y1/math.tan(self.angle_wrt_x_axis)
        #
        # y2 = y1+50
        # x2 = x1+50
        #
        # print("AFTER {},{},{},{}".format(x1,y1,x2,y2))

        if self.direction == Direction.UP:
            self.dy = -Ball.PIXEL_PER_MOVE
        if self.direction == Direction.DOWN:
            self.dy = Ball.PIXEL_PER_MOVE

        if self.angle_wrt_x_axis:
            self.dx = (self.dy) / math.tan(math.radians(self.angle_wrt_x_axis))
        else:
            self.dx = 0

        # print(self.angle_wrt_x_axis)
        # print("{},{}".format(self.dx, self.dy))

        # self.parent.coords(self.canvas_index, *(x1,y1,x2,y2))
        self.parent.move(self.canvas_index, self.dx, self.dy)
        self.parent.update()

        new_cords = self.parent.coords(self.canvas_index)[0], self.parent.coords(self.canvas_index)[1]

        # self.parent.create_line(prev_cords, new_cords)

        # x1, y1 = self.coords[0]+self.dx, self.coords[1]+self.dy
        #
        # x2,y2 = self.coords[2]+self.dx, self.coords[3]+self.dy
        #
        # self.coords = (x1,y1, x2, y2)

        self.parent.after(self.speed, self.move)

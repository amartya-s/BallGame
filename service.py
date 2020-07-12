import random

from BallGame.ball import Ball
from BallGame.direction import Direction
from BallGame.player import Player


class GameService(object):
    BALL_INDEXES = []
    BALLS_BY_INDEXES = dict()

    def __init__(self, game_canvas, score_var):
        self.canvas = game_canvas
        self.player = None
        self.ball_diameter = 40
        self.score_var = score_var

    def initialize(self):
        self.bind_events()
        print("Event bind Done")

    def add_player(self):
        # add player at 3/4th of window height
        x_cord = self.canvas.width / 2
        y_cord = self.canvas.height * (3 / 4)

        self.player = Player(self.canvas, 70, 20, x_cord, y_cord)

    def add_ball(self):
        for i in range(0, 5):
            ball = Ball(self.canvas, random.randint(0, 20), self.ball_collision_callback_fn, *(
            (350 + i * 50) % self.canvas.width, 100, (350 + i * 50) % self.canvas.width + self.ball_diameter,
            100 + self.ball_diameter))
            ball.direction = Direction.DOWN
            ball.angle_wrt_x_axis = 70 + random.randint(-100, 100)
            ball.move()

            GameService.BALL_INDEXES.append(ball)
            GameService.BALLS_BY_INDEXES[ball.canvas_index] = ball
            print("Ball Created")

    def move_player(self, event):
        print(event.keysym)
        self.player.move(event.keysym, 40)

    def ball_collision_callback_fn(self, ball):
        ball_coords = self.canvas.coords(ball.canvas_index)
        overlapping_objs = self.canvas.find_overlapping(*ball_coords)

        ball_with_ball_collisions = set(overlapping_objs) - {ball.canvas_index, self.player.canvas_index}
        for ball_canvas_index in ball_with_ball_collisions:
            target_ball = GameService.BALLS_BY_INDEXES[ball_canvas_index]

            source_ball_speed = ball.speed
            target_ball_speed = target_ball.speed

            mid_speed = int((source_ball_speed + target_ball_speed) / 2)

            target_ball.speed = mid_speed
            ball.speed = mid_speed

            target_ball.angle_wrt_x_axis = -target_ball.angle_wrt_x_axis
            ball.angle_wrt_x_axis = -ball.angle_wrt_x_axis

        if not {self.player.canvas_index, ball.canvas_index} - set(list(overlapping_objs)):
            # self.canvas.create_line(ball_coords[0], ball_coords[1]-100, ball_coords[0], ball_coords[1]+100)
            ball.direction = Direction.UP
            ball.angle_wrt_x_axis = -ball.angle_wrt_x_axis
            self.score_var.set("{}".format(int(self.score_var.get()) + 1))

        elif ball_coords[1] == 0 or ball_coords[3] == 0:
            ball.direction = Direction.DOWN
            ball.angle_wrt_x_axis = -ball.angle_wrt_x_axis


        elif ball_coords[2] >= self.canvas.width or ball_coords[0] <= 0:

            ball.angle_wrt_x_axis = - ball.angle_wrt_x_axis

            # self.canvas.create_line(ball_coords[0]-100, ball_coords[1], ball_coords[0]+100, ball_coords[1])

        elif (ball_coords[1] == self.canvas.height):
            print("Ball {} destroyed".format(ball.canvas_index))
            del GameService.BALLS_BY_INDEXES[ball.canvas_index]
            self.canvas.delete(ball.canvas_index)
            del ball

            # ball.direction = Direction.UP
            # ball.angle_wrt_x_axis = -ball.angle_wrt_x_axis
            # self.canvas.create_line(ball_coords[0], ball_coords[1], ball_coords[0], ball_coords[1]-100)

    def bind_events(self):
        print(self.canvas.master.master)
        self.canvas.master.master.bind("<KeyPress-Left>", lambda e: self.move_player(e))
        self.canvas.master.master.bind("<KeyPress-Right>", lambda e: self.move_player(e))
        self.canvas.master.master.bind("<KeyPress-Up>", lambda e: self.move_player(e))
        self.canvas.master.master.bind("<KeyPress-Down>", lambda e: self.move_player(e))

    def start_game(self):
        self.add_player()
        self.add_ball()

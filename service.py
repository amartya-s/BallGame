import random
import time

from BallGame.ball import Ball
from BallGame.direction import Direction
from BallGame.player import Player
from BallGame.bullet import Bullet


class GameService(object):
    BALL_INDEXES = []
    BALLS_BY_INDEXES = dict()
    BULLET_DIAMETER = 10

    def __init__(self, game, score_var):
        self.canvas = game.game_canvas
        self.status_label = game.status_label
        self.player = None
        self.ball_diameter = 40
        self.score_var = score_var
        self.game_over_status = False

    def initialize(self):
        self.bind_events()
        print("Event bind Done")

    def add_player(self):
        # add player at 3/4th of window height
        x_cord = self.canvas.width / 2
        y_cord = self.canvas.height * (3 / 4)

        self.player = Player(self.canvas, 70, 20, x_cord, y_cord)

    def add_ball(self):
        if  self.game_over_status:
            return

        x1_cord = random.randint(0, self.canvas.width)
        y1_cord = random.randint(10,20)

        coords = (x1_cord, y1_cord, x1_cord+self.ball_diameter, y1_cord+self.ball_diameter)

        ball = Ball(self.canvas, random.randint(30, 50), self.ball_collision_callback_fn, *coords)
        ball.direction = Direction.DOWN
        ball.angle_wrt_x_axis = random.randint(0, 189)
        ball.move()

        GameService.BALL_INDEXES.append(ball.canvas_index)
        GameService.BALLS_BY_INDEXES[ball.canvas_index] = ball
        print("Ball Created")

        # add balls at random interval of 500 to 1000ms
        self.canvas.after(random.randint(500, 1000), lambda: self.add_ball())

    def move_player(self, event):
        print(event.keysym)
        self.player.move(event.keysym, 40)

    def shoot(self):
        if self.player.is_frozen:
            return

        player_cords = self.player.player_surrounding_rectangle_coords
        bullet_center = ((player_cords[0] + player_cords[2]) / 2, (player_cords[1] + player_cords[3]) / 2)

        bullet = Bullet(self.canvas, self.bullet_collision_callback_fn, *bullet_center)

        self.player.shoot(bullet)

    def check_collision_with_player(self, ball):
        px1, py1, px2, py2 = self.player.player_surrounding_rectangle_coords()
        bx1, by1, bx2, by2 = self.canvas.coords(ball.canvas_index)

        direction = ball.direction
        angle = ball.angle_wrt_x_axis

        # top on collision
        if py1 >= by2:
            direction = Direction.UP
        # if px1 <= bx ,/

    def bullet_collision_callback_fn(self, bullet):
        bullet_coords = self.canvas.coords(bullet)

        overlapping_objs = set(self.canvas.find_overlapping(*bullet_coords))

        overlapping_balls = overlapping_objs.intersection(GameService.BALL_INDEXES)

        # pick the first one
        if overlapping_balls:
            overlapping_ball = overlapping_balls.pop()

            # destroy ball and bullet
            self.canvas.delete(bullet)

            ball_obj=GameService.BALLS_BY_INDEXES[overlapping_ball]
            ball_obj.destroy()

            self.score_var.set("{}".format(int(self.score_var.get()) + 1))

            return True

        return False

    def ball_collision_callback_fn(self, ball):
        ball_coords = self.canvas.coords(ball.canvas_index)
        overlapping_objs = self.canvas.find_overlapping(*ball_coords)

        ball_with_ball_collisions = set(overlapping_objs) - {ball.canvas_index, self.player.canvas_index}
        # for ball_canvas_index in ball_with_ball_collisions:
        #     target_ball = GameService.BALLS_BY_INDEXES[ball_canvas_index]
        #
        #     source_ball_speed = ball.speed
        #     target_ball_speed = target_ball.speed
        #
        #     mid_speed = int((source_ball_speed + target_ball_speed) / 2)
        #
        #     target_ball.speed = mid_speed
        #     ball.speed = mid_speed
        #
        #     target_ball.angle_wrt_x_axis = -target_ball.angle_wrt_x_axis
        #     ball.angle_wrt_x_axis = -ball.angle_wrt_x_axis

        if self.player.canvas_index in overlapping_objs:
            if not ball.in_collision:
            #     ball.direction = Direction.UP
            #     ball.angle_wrt_x_axis = -ball.angle_wrt_x_axis
            #     ball.in_collision = True

                self.end_game()

        else:
            ball.in_collision = False

        if ball_coords[1] == 0 or ball_coords[3] == 0:
            ball.direction = Direction.DOWN
            ball.angle_wrt_x_axis = -ball.angle_wrt_x_axis

        elif ball_coords[2] >= self.canvas.width or ball_coords[0] <= 0:

            ball.angle_wrt_x_axis = - ball.angle_wrt_x_axis

            # self.canvas.create_line(ball_coords[0]-100, ball_coords[1], ball_coords[0]+100, ball_coords[1])

        elif (ball_coords[1] == self.canvas.height):
            print("Ball {} destroyed".format(ball.canvas_index))

            ball_obj = GameService.BALLS_BY_INDEXES[ball.canvas_index]
            ball_obj.destroy()

            self.end_game()

            #del ball_obj

            # ball.angle_wrt_x_axis = -ball.angle_wrt_x_axis
            # self.canvas.create_line(ball_coords[0], ball_coords[1], ball_coords[0], ball_coords[1]-100)

    def bind_events(self):
        print(self.canvas.master.master)
        self.canvas.bind_all("<KeyPress-Left>", lambda e: self.move_player(e))
        self.canvas.bind_all("<KeyPress-Right>", lambda e: self.move_player(e))
        self.canvas.bind_all("<KeyPress-Up>", lambda e: self.move_player(e))
        self.canvas.bind_all("<KeyPress-Down>", lambda e: self.move_player(e))

        self.canvas.bind_all("<space>", lambda e: self.shoot())
        self.canvas.bind_all("<Button-1>", lambda e: self.shoot())

    def start_game(self):
        self.add_player()
        self.add_ball()

    def end_game(self):
        print(self.status_label)
        self.status_label['text'] = 'Game Over'
        self.status_label['bg'] = 'red'

        self.game_over_status = True

        self.player.freeze()

        # Stop all balls
        for index, ball in GameService.BALLS_BY_INDEXES.items():
            print("Stopping ball: {}".format(index))
            ball.freeze()


from BallGame.direction import Direction


class Bullet(object):
    BULLET_RADIUS = 10

    def __init__(self,canvas, collision_callback_fc, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.collision_callback = collision_callback_fc

        self.bullet = self.create_bullet()

    def create_bullet(self):
        bullet_coord = (self.x - Bullet.BULLET_RADIUS, self.y - Bullet.BULLET_RADIUS, self.x + Bullet.BULLET_RADIUS, \
                       self.y + Bullet.BULLET_RADIUS)

        bullet = self.canvas.create_oval(bullet_coord, fill='red')

        return bullet

    def move(self, direction):
        if self.collision_callback(self.bullet):
            return
        if self.y <= 0:
            self.canvas.delete(self.bullet)
            return
        if direction == Direction.UP:
            self.canvas.move(self.bullet, 0, -1)
            self.y -= 1

        self.canvas.after(5, lambda: self.move(direction))

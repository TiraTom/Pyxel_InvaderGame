import os
import pyxel
import random
from enum import IntEnum, auto

WINDOW_HEIGHT = 160
WINDOW_WIDTH = 120

class Direction(IntEnum):
    Up = auto()
    Down = auto()
    Right = auto()
    Left = auto()


class Ball:

    def __init__(self):
        self.x = 60
        self.y = 110
        self.r = 2
        self.direction = Direction.Down
        self.center = (self.x + self.r) / 2

    def draw(self):
        pyxel.circ(self.x, self.y, self.r, 8)



class Wall:
    def __init__(self):
        self.x = 52
        self.y = 145
        self.height = 5
        self.width = 16
        self.color = 8

    def draw(self):
        pyxel.rect(self.x, self.y, self.x + self.width, self.y + self.height, self.color)

    def move_right(self):
        # 右の壁にぶつかってない場合は移動
        if self.x + self.width < WINDOW_WIDTH:
            self.x = self.x + 1

    def move_left(self):
        # 左の壁にぶつかってない場合は移動
        if 0 < self.x:
            self.x = self.x - 1


class Block:

    def __init__(self):
        # ★TODO 記述を簡潔にする
        self.block1 = [[(12 + 12 * i), 15, 9, 4, random.randint(10,15)] for i in range(8)]
        self.block2 = [[(18 + 12 * i), 23, 9, 4, random.randint(10,15)] for i in range(7)]
        self.block3 = [[(12 + 12 * i), 31, 9, 4, random.randint(10,15)] for i in range(8)]
        self.block4 = [[(18 + 12 * i), 39, 9, 4, random.randint(10,15)] for i in range(7)]
        self.block5 = [[(12 + 12 * i), 47, 9, 4, random.randint(10,15)] for i in range(8)]
        self.block6 = [[(18 + 12 * i), 55, 9, 4, random.randint(10,15)] for i in range(7)]
        self.blocks = self.block1 + self.block2 + self.block3 + self.block4 + self.block5 + self.block6

    def draw(self):
        [pyxel.rect(block[0], block[1], block[0] + block[2], block[1] + block[3], block[4]) for block in self.blocks]



class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, caption="BlockGame")

        # pyxel.load(f'{os.path.dirname(__file__)}/assets/block_game.pyxel')

        self.ball = Ball()
        self.wall = Wall()
        self.block = Block()

        pyxel.run(self.update, self.draw)


    def move_direction_check(self, ball, wall, block):
        # ブロックとの衝突判定


        # wallとの衝突判定
        if wall.x <= ball.x and ball.x <= (wall.x + wall.width) and ball.y + 1 == wall.y:
            ball.direction = Direction.Up

        # y軸方向についての処理
        if ball.y - 1 == 0:
            ball.direction = Direction.Down

        if ball.direction == Direction.Down:
            ball.y = ball.y + 1

        if ball.direction == Direction.Up:
            ball.y = ball.y - 1

        if ball.x + 1 == WINDOW_WIDTH:
            ball.direction = Direction.Left

        if ball.x - 1 == 0:
            ball.direction = Direction.Right


        if ball.direction == Direction.Right:
            ball.x = ball.x + 1

        if ball.direction == Direction.Left:
            ball.x = ball.x - 1



    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_LEFT):
            self.wall.move_left()

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.wall.move_right()

        self.move_direction_check(self.ball, self.wall, self.block)



    def draw(self):
        pyxel.cls(0)

        self.ball.draw()
        self.wall.draw()
        self.block.draw()

        if self.ball.y >= WINDOW_HEIGHT:
            pyxel.text(60, 110, "You Failed", 5)


App()






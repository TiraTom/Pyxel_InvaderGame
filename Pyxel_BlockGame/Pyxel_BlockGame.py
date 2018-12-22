import os
import pyxel
import random
import sys
from msvcrt import getch
from enum import IntEnum, auto

WINDOW_HEIGHT = 160
WINDOW_WIDTH = 120

class Direction(IntEnum):
    Up = auto()
    Down = auto()
    Right = auto()
    Center = auto()
    Left = auto()


class Ball:

    def __init__(self):
        self.x = 60
        self.y = 110
        self.r = 2
        self.direction_x = Direction.Center
        self.direction_y = Direction.Down
        self.center = (self.x + self.r) / 2

    def draw(self):
        pyxel.circ(self.x, self.y, self.r, 8)

    def update(self):
        if self.direction_y == Direction.Up:
            self.y = self.y - 1

        if self.direction_y == Direction.Down:
            self.y = self.y + 1

        if self.direction_x == Direction.Right:
            self.x = self.x + 1

        if self.direction_x == Direction.Left:
            self.x = self.x - 1



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


    def ball_direction_update(self, ball, wall, block):
        # ブロックとの衝突判定


        # y軸方向の処理
        if wall.x <= ball.x and ball.x <= (wall.x + wall.width) and ball.y + 1 == wall.y:
            ball.direction_y = Direction.Up

        if ball.y - 1 == 0:
            ball.direction_y = Direction.Down

        # x軸方向の処理
        if ball.x + 1 == WINDOW_WIDTH:
            ball.direction_x = Direction.Left

        if ball.x - 1 == 0:
            ball.direction_x = Direction.Right





    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_LEFT):
            self.wall.move_left()

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.wall.move_right()

        self.ball_direction_update(self.ball, self.wall, self.block)

        self.ball.update()



    def draw(self):
        pyxel.cls(0)

        self.ball.draw()
        self.wall.draw()
        self.block.draw()

        if self.ball.y - 2 > WINDOW_HEIGHT:
            pyxel.text(60, 110, "You Failed", 5)

            #if ord(getch()) == 13:
            #    pyxel.quit()


print(" Start New Game : Press Enter Key")
print(" Quit Game : Press Q Key")

if ord(getch()) == 13:
    App()

while True:
    if ord(getch()) == 113:
        break

    App()

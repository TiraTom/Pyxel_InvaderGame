import os
import pyxel
import random
import sys
from msvcrt import getch
from enum import IntEnum, auto

WINDOW_HEIGHT = 160
WINDOW_WIDTH = 120
FIGHTER_Y = 145
FIGHTER_WIDTH = 7
FIGHTER_HEIGHT = 4

class Direction(IntEnum):
    Up = auto()
    Down = auto()
    Right = auto()
    Center = auto()
    Left = auto()


class Shot():

    def __init__(self, position_x):
        self.x = position_x
        self.y = FIGHTER_Y
        self.color = 8
        self.alive = True

    def draw(self):
        pyxel.pix(self.x, self.y, self.color)

    def update(self, enemy):
        self.y = self.y + 1

        if self.y == 0:
            self.alive = False

        if self.alive:
            self.draw()




class Fighter:
    def __init__(self):
        self.x = WINDOW_WIDTH / 2 + FIGHTER_WIDTH / 2
        self.y = FIGHTER_Y
        self.shot_x = self.x + FIGHTER_WIDTH / 2
        self.alive = True

    def draw(self):
        pyxel.blt(self.x, self.y, 1, 0, 0, FIGHTER_WIDTH, FIGHTER_HEIGHT, 13)

    def move_right(self):
        # 右の壁にぶつかってない場合は移動
        if self.x + FIGHTER_WIDTH < WINDOW_WIDTH:
            self.x = self.x + 1

    def move_left(self):
        # 左の壁にぶつかってない場合は移動
        if 0 < self.x:
            self.x = self.x - 1

    def shot(self, x):
        shot = Shot(self.x)
        while(shot.alive):
            shot.update()



class EnemyInfo:
    __init__(self):
        self.x
        self.y
        self.color
        self.hp


class Enemy:

    def __init__(self):

        # ★TODO 記述を簡潔にする
        self.enemy1 = [[(12 + 12 * i), 15, 9, 4, random.randint(10,15)] for i in range(4)]
        self.enemy2 = [[(18 + 12 * i), 23, 9, 4, random.randint(10,15)] for i in range(4)]
        self.enemy3 = [[(12 + 12 * i), 31, 9, 4, random.randint(10,15)] for i in range(4)]
        self.enemy4 = [[(18 + 12 * i), 39, 9, 4, random.randint(10,15)] for i in range(4)]
        self.enemy = self.enemy1 + self.enemy2 + self.enemy3 + self.enemy4 + self.enemy5

    def draw(self):
        [pyxel.blt(block[0])]
        [pyxel.rect(block[0], block[1], block[0] + block[2], block[1] + block[3], block[4]) for block in self.blocks]



class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, caption="InvaderGame")

        pyxel.load(f'{os.path.dirname(__file__)}/assets/invade_game.pyxel')

        self.fighter = Fighter()
        self.enemy = Enemy()

        pyxel.run(self.update, self.draw)


    def enemy_hit_check(self, enemy, shots):
        # 撃墜判定



    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.shots.append(Shot(self.fighter.x))

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_LEFT):
            self.fighter.move_left()

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.fighter.move_right()

        self.enemy_hit_check(self.enemy, self.shots)

        self.ball.update()



    def draw(self):
        pyxel.cls(0)

        self.ball.draw()
        self.wall.draw()
        self.block.draw()

        if self.fighter.alive == False:
            pyxel.text(WINDOW_WIDTH / 2 + FIGHTER_WIDTH / 2, WINDOW_HEIGHT / 3 * 2, "You Failed", 5)

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

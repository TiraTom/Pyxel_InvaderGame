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
FIGHTER_DATA_POSITION = ()
ENEMY_HEIGHT = 4
ENEMY_WIDTH = 4
ENEMY_DATA_POSITION = ()

class Direction(IntEnum):
    Up = auto()
    Down = auto()
    Right = auto()
    Center = auto()
    Left = auto()

class Level(IntEnum):
    Weak = auto()
    Normal = auto()
    Strong = auto()

class Shot():

    def __init__(self, position_x):
        self.x = position_x
        self.status = Status.Valid
        self.color

    def draw(self):
        pyxel.pix(self.x, self.y, self.color)

    def update(self):
        if self.y == 0 or self.y == WINDOW_HEIGHT: 
            self.status = Status.Invalid

        if self.alive:
            self.draw()

class FighterShot(Shot):
    def __init__(self, position_x):
        super().__init__(position_x)
        self.y = FIGHTER_Y
        self.color = 8

    def update(self):
        self.y = self.y - 1
        super().update()



class EnemyShot(Shot):
    def __init__(self, position_x, position_y):
        super().__init__(position_x)
        self.y =  position_y
        self.color = 4

    def update(self):
        self.y = self.y + 1
        super().update()








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



class Enemy:
    def __init__(self, x, y, level):
        self.x
        self.y
        self.color
        self.hp
        self.status = Status.Valid

        if level == Level.Weak:
            self.color = 9
            self.hp = 1
        if level == Level.Normal:
            self.color = 11
            self.hp = 2
        if level == Level.Strong:
            self.color = 14
            self.hp = 3

    def hit(self):
        self.hp = self.hp - 1

        if self.hp == 0:
            self.status = Status.Invalid



class Enemies:

    def __init__(self):

        self.raw1 = [Enemy(5 + (ENEMY_WIDTH + 3) * i, 5, 3) for i in range(4)]
        self.raw2 = [Enemy(5 + (ENEMY_WIDTH + 3) * i, 5 + ENEMY_HEIGHT + 3, 2) for i in range(4)]
        self.raw3 = [Enemy(5 + (ENEMY_WIDTH + 3) * i,  5 + (ENEMY_HEIGHT + 3) * 2 , 1) for i in range(4)]

        self.enemy_group = raw1 + raw2 + raw3

    def draw(self):
        [pyxel.blt(enemy.x, enemy_y, ) for enemy in self.enemy_group]
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

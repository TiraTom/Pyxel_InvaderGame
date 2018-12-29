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
FIGHTER_HEIGHT = 8
FIGHTER_DATA_POSITION = (0, 0)
ENEMY_HEIGHT = 6
ENEMY_WIDTH = 7
ENEMY_DATA1_POSITION = (8, 0)
ENEMY_DATA2_POSITION = (0, 9)
ENEMY_DATA3_POSITION = (9, 9)
SHOT_POSITION = (16, 0)
SHOT_HEIGHT = 7
SHOT_WIDTH = 7

class Status(IntEnum):
    Valid = auto()
    Invalid = auto()

class Level(IntEnum):
    Weak = auto()
    Normal = auto()
    Strong = auto()

class Shot():

    def __init__(self, position_x):
        self.x = position_x
        self.y = 0
        self.color = 0
        self.status = Status.Valid

    def draw(self):
        if self.status == Status.Valid:
            pyxel.pix(self.x, self.y, self.color)

    def update(self):
        if self.y == 0 or self.y == WINDOW_HEIGHT: 
            self.status = Status.Invalid


class FighterShot(Shot):
    def __init__(self, position_x):
        super().__init__(position_x + FIGHTER_WIDTH / 2)
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
        self.x = WINDOW_WIDTH / 2 - FIGHTER_WIDTH / 2
        self.y = FIGHTER_Y
        self.shot_x = self.x + FIGHTER_WIDTH / 2
        self.status = Status.Valid

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, FIGHTER_WIDTH, FIGHTER_HEIGHT, 13)

    def move_right(self):
        # 右の壁にぶつかってない場合は移動
        if self.x + FIGHTER_WIDTH + 1 < WINDOW_WIDTH:
            self.x = self.x + 1

    def move_left(self):
        # 左の壁にぶつかってない場合は移動
        if 0 < self.x:
            self.x = self.x - 1



class Enemy:
    def __init__(self, x, y, level):
        self.x = x
        self.y = y
        self.status = Status.Valid

        if level == Level.Weak:
            self.hp = 1
            self.picture_position_x = ENEMY_DATA1_POSITION[0]
            self.picture_position_y = ENEMY_DATA1_POSITION[1]
        if level == Level.Normal:
            self.hp = 2
            self.picture_position_x = ENEMY_DATA2_POSITION[0]
            self.picture_position_y = ENEMY_DATA2_POSITION[1]
        if level == Level.Strong:
            self.hp = 3
            self.picture_position_x = ENEMY_DATA3_POSITION[0]
            self.picture_position_y = ENEMY_DATA3_POSITION[1]

    def hit(self):
        self.hp = self.hp - 1

        if self.hp == 0:
            self.status = Status.Invalid

    def update(self):
        if pyxel.frame_count % 20 == 0:
            self.x = self.x + 3 
        elif pyxel.frame_count % 20 == 5:
            self.x = self.x - 3
        elif pyxel.frame_count % 20 == 10:
            self.x = self.x - 3
        elif pyxel.frame_count % 20 == 15:
            self.x = self.x + 3



class EnemyList:

    def __init__(self):

        self.raw1 = [Enemy(10 + (ENEMY_WIDTH + 3) * i, 7, 3) for i in range(10)]
        self.raw2 = [Enemy(10 + (ENEMY_WIDTH + 3) * i, 7 + ENEMY_HEIGHT + 7, 2) for i in range(10)]
        self.raw3 = [Enemy(10 + (ENEMY_WIDTH + 3) * i,  7 + (ENEMY_HEIGHT + 7) * 2 , 1) for i in range(10)]

        self.enemy_group = self.raw1 + self.raw2 + self.raw3

    def draw(self):
        [pyxel.blt(enemy.x, enemy.y, 0, enemy.picture_position_x, enemy.picture_position_y, ENEMY_WIDTH, ENEMY_HEIGHT, 13) for enemy in self.enemy_group]

    def update(self):
        a = 1


class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, caption="InvaderGame")

        pyxel.load(f'{os.getcwd()}/resource_file.pyxel')

        self.fighter = Fighter()
        self.enemy_list = EnemyList()
        self.shot_list = []

        pyxel.run(self.update, self.draw)

        


    def enemy_hit_check(self, fighter, senemy_list, shot_list):
        # 撃墜判定
        if 1 == 1:
            fighter.stauts = Status.Invalid
        else:
            fighter.stauts = Status.Valid



    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.shot_list.append(FighterShot(self.fighter.x))

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_LEFT):
            self.fighter.move_left()

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.fighter.move_right()

        self.enemy_hit_check(self.fighter, self.enemy_list, self.shot_list)

        self.enemy_list.update()

        if len(self.shot_list) > 0:
            [shot.update() for shot in self.shot_list]



    def draw(self):
        pyxel.cls(0)

        self.fighter.draw()
        self.enemy_list.draw()

        if len(self.shot_list) > 0:
            [shot.draw() for shot in self.shot_list]

        if self.fighter.status == Status.Invalid:
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

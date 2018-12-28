import os
import pyxel
import random
import sys
from msvcrt import getch
from enum import IntEnum, auto

WINDOW_HEIGHT = 160
WINDOW_WIDTH = 120
FIGHTER_Y = 145
FIGHTER_WIDTH = 6
FIGHTER_HEIGHT = 7
FIGHTER_DATA_POSITION = (0, 0)
ENEMY_HEIGHT = 6
ENEMY_WIDTH = 6
ENEMY_DATA1_POSITION = (8, 0)
ENEMY_DATA2_POSITION = (0, 8)
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


class ShotList():
    def __init__(self):
        a = True

    def update(self):
        b = True

    def draw(self):
        c = True





class Fighter:
    def __init__(self):
        self.x = WINDOW_WIDTH / 2 + FIGHTER_WIDTH / 2
        self.y = FIGHTER_Y
        self.shot_x = self.x + FIGHTER_WIDTH / 2
        self.status = Status.Valid

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
        self.x = x
        self.y = y
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

        self.raw1 = [Enemy(5 + (ENEMY_WIDTH + 3) * i, 5, 3) for i in range(4)]
        self.raw2 = [Enemy(5 + (ENEMY_WIDTH + 3) * i, 5 + ENEMY_HEIGHT + 3, 2) for i in range(4)]
        self.raw3 = [Enemy(5 + (ENEMY_WIDTH + 3) * i,  5 + (ENEMY_HEIGHT + 3) * 2 , 1) for i in range(4)]

        self.enemy_group = self.raw1 + self.raw2 + self.raw3

    def draw(self):
        b = 1
        #[pyxel.blt(enemy.x, enemy_y, ) for enemy in self.enemy_group]
        #[pyxel.rect(block[0], block[1], block[0] + block[2], block[1] + block[3], block[4]) for block in self.blocks]

    def update(self):
        a = 1


class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, caption="InvaderGame")

        pyxel.load(f'{os.getcwd()}/resource_file.pyxel')

        self.fighter = Fighter()
        self.enemy_list = EnemyList()
        self.shot_list = ShotList()

        pyxel.run(self.update, self.draw)


    def enemy_hit_check(self, fighter, senemy_list, shot_list):
        # 撃墜判定
        if 1 == 1:
            fighter.stauts = Status.Invalid
        else:
            fighter.stauts = Status.Valid



    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.shot_list.append(Shot(self.fighter.x))

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_LEFT):
            self.fighter.move_left()

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.fighter.move_right()

        self.enemy_hit_check(self.fighter, self.enemy_list, self.shot_list)

        self.enemy_list.update()
        self.shot_list.update()



    def draw(self):
        pyxel.cls(0)

        self.fighter.draw()
        self.enemy_list.draw()
        self.shot_list.draw()

        if self.fighter.status == False:
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

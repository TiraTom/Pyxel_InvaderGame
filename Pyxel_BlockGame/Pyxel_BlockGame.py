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
WEAPON_NUMBER = 7

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
        if self.x + FIGHTER_WIDTH + 1 < WINDOW_WIDTH:
            self.x = self.x + 1

    def move_left(self):
        if 0 < self.x:
            self.x = self.x - 1



class Enemy:
    def __init__(self, x, y, level):
        self.x = x
        self.y = y

        if level == Level.Weak:
            self.hp = 1
            self.picture_position_x = ENEMY_DATA1_POSITION[0]
            self.picture_position_y = ENEMY_DATA1_POSITION[1]
            self.score = 5
        if level == Level.Normal:
            self.hp = 2
            self.picture_position_x = ENEMY_DATA2_POSITION[0]
            self.picture_position_y = ENEMY_DATA2_POSITION[1]
            self.score = 10
        if level == Level.Strong:
            self.hp = 3
            self.picture_position_x = ENEMY_DATA3_POSITION[0]
            self.picture_position_y = ENEMY_DATA3_POSITION[1]
            self.score = 15

    def update(self):
        if pyxel.frame_count % 100 == 0:
            self.x = self.x + 3 
        elif pyxel.frame_count % 100 == 25:
            self.x = self.x - 3
        elif pyxel.frame_count % 100 == 50:
            self.x = self.x - 3
        elif pyxel.frame_count % 100 == 75:
            self.x = self.x + 3



class EnemyList:

    def __init__(self):

        self.raw1 = [Enemy(10 + (ENEMY_WIDTH + 5) * i, 15, 3) for i in range(9)]
        self.raw2 = [Enemy(10 + (ENEMY_WIDTH + 5) * i, 15 + ENEMY_HEIGHT + 7, 2) for i in range(9)]
        self.raw3 = [Enemy(10 + (ENEMY_WIDTH + 5) * i, 15 + (ENEMY_HEIGHT + 7) * 2 , 1) for i in range(9)]

        self.enemy_group = self.raw1 + self.raw2 + self.raw3

    def draw(self):
        [pyxel.blt(enemy.x, enemy.y, 0, enemy.picture_position_x, enemy.picture_position_y, ENEMY_WIDTH, ENEMY_HEIGHT, 13) for enemy in self.enemy_group]

    def update(self):
        if pyxel.frame_count % 1000 == 999:
            for enemy in self.enemy_group:
                enemy.y = enemy.y + ENEMY_HEIGHT

        [enemy.update() for enemy in self.enemy_group]


class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, caption="InvaderGame")

        pyxel.load(f'{os.getcwd()}/resource_file.pyxel')

        self.fighter = Fighter()
        self.enemy_list = EnemyList()
        self.shot_list = []

        self.score = 0

        pyxel.run(self.update, self.draw)

        


    def enemy_hit_check(self, fighter, enemy_list, shot_list):
        # 撃墜判定
        for shot in shot_list:
            for enemy in enemy_list.enemy_group:
                if shot.status == Status.Valid \
                    and 0 < enemy.hp:
                    if enemy.x <= shot.x \
                        and shot.x <= enemy.x + ENEMY_WIDTH \
                        and enemy.y <= shot.y \
                        and shot.y <= enemy.y + ENEMY_HEIGHT:
                        enemy.hp = enemy.hp - 1
                        shot.status = Status.Invalid
                        if enemy.hp == 0:
                            self.score = self.score + enemy.score

        for enemy in enemy_list.enemy_group:
            if enemy.x <= fighter.x \
                and fighter.x + FIGHTER_WIDTH <= enemy.x \
                and enemy.y <= fighter.y \
                and fighter.y + FIGHTER_HEIGHT <= enemey.y:
                fighter.status = Status.Invalid

        self.enemy_list.update()

        # 無効になった敵を削除する処理
        for enemy in enemy_list.enemy_group:
            if enemy.hp == 0 :
                enemy_list.enemy_group.remove(enemy)

        # 無効になった弾を削除する処理
        for shot in shot_list:
            if shot.status == Status.Invalid:
                shot_list.remove(shot)
        



    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            if len(self.shot_list) <= WEAPON_NUMBER :
                self.shot_list.append(FighterShot(self.fighter.x))

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_LEFT):
            self.fighter.move_left()

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.fighter.move_right()

        self.enemy_hit_check(self.fighter, self.enemy_list, self.shot_list)


        if len(self.shot_list) > 0:
            [shot.update() for shot in self.shot_list]

        if len(self.enemy_list.enemy_group) == 0:
            pyxel.text(WINDOW_WIDTH / 2 - 20, WINDOW_HEIGHT / 2 - 10 , 'Clear!!!', 6)



    def draw(self):
        pyxel.cls(0)

        pyxel.text(10, 3, f'score = {self.score}', 2)

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

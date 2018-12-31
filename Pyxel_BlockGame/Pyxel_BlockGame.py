import os
import pyxel
import random
import sys
import numpy as np
from msvcrt import getch
from enum import IntEnum, auto, Enum


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
WEAPON_NUMBER = 5
FIGHTER_SHOT_SPEED = 2

class Status(IntEnum):
    Valid = auto()
    Invalid = auto()

class Level(Enum):
    Weak = 1
    Normal = 2
    Strong = 3

class Shot():

    def __init__(self, position_x):
        self.x = position_x
        self.y = 0
        self.color = 0
        self.status = Status.Valid

    def update(self):
        if self.y <= 0 or WINDOW_HEIGHT <= self.y: 
            self.status = Status.Invalid


class FighterShot(Shot):
    def __init__(self, position_x):
        super().__init__(position_x + FIGHTER_WIDTH / 2)
        self.y = FIGHTER_Y
        self.color = 8
        self.speed = FIGHTER_SHOT_SPEED

    def update(self):
        self.y = self.y - self.speed
        super().update()

    def draw(self):
        if self.status == Status.Valid:
            pyxel.pix(self.x, self.y, self.color)
            pyxel.pix(self.x, self.y + 1, 7)




class EnemyShot(Shot):
    def __init__(self, position_x, position_y, speed):
        super().__init__(position_x)
        self.y =  position_y
        self.color = 10
        self.speed = speed

    def update(self):
        self.y = self.y + self.speed
        super().update()

    def draw(self):
        if self.status == Status.Valid:
            pyxel.pix(self.x, self.y, self.color)
            pyxel.pix(self.x, self.y - 1, 7)



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
            self.level = Level.Weak.value
            self.shot_speed = 2
        if level == Level.Normal:
            self.hp = 2
            self.picture_position_x = ENEMY_DATA2_POSITION[0]
            self.picture_position_y = ENEMY_DATA2_POSITION[1]
            self.score = 10
            self.level = Level.Normal.value
            self.shot_speed = 3
        if level == Level.Strong:
            self.hp = 3
            self.picture_position_x = ENEMY_DATA3_POSITION[0]
            self.picture_position_y = ENEMY_DATA3_POSITION[1]
            self.score = 15
            self.level = Level.Strong.value
            self.shot_speed = 5

    def update(self):
        if pyxel.frame_count % 120 == 15:
            self.x = self.x + 5 
        elif pyxel.frame_count % 120 == 45:
            self.x = self.x - 5
        elif pyxel.frame_count % 120 == 75:
            self.x = self.x - 5
        elif pyxel.frame_count % 120 == 105:
            self.x = self.x + 5




class EnemyList:

    def __init__(self):

        self.raw1 = [Enemy(9 + (ENEMY_WIDTH + 5) * i, 15, Level.Strong) for i in range(9)]
        self.raw2 = [Enemy(9 + (ENEMY_WIDTH + 5) * i, 15 + ENEMY_HEIGHT + 7, Level.Normal) for i in range(9)]
        self.raw3 = [Enemy(9 + (ENEMY_WIDTH + 5) * i, 15 + (ENEMY_HEIGHT + 7) * 2 , Level.Weak) for i in range(9)]

        self.enemy_group = self.raw1 + self.raw2 + self.raw3

    def draw(self):
        [pyxel.blt(enemy.x, enemy.y, 0, enemy.picture_position_x, enemy.picture_position_y, ENEMY_WIDTH, ENEMY_HEIGHT, 13) for enemy in self.enemy_group]

    def update(self):
        if pyxel.frame_count % 1000 == 999:
            for enemy in self.enemy_group:
                enemy.y = enemy.y + ENEMY_HEIGHT

        [enemy.update() for enemy in self.enemy_group]

        if pyxel.frame_count % 200 == 199:
            a = 1


class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, caption="InvaderGame")

        pyxel.load(f'{os.getcwd()}/resource_file.pyxel')

        self.fighter = Fighter()
        self.enemy_list = EnemyList()
        self.shot_list = []
        self.score = 0

        pyxel.run(self.update, self.draw)
        

    def did_enemy_shot_fighter(self, shot, fighter):
        if fighter.x <= shot.x \
        and shot.x <= fighter.x + FIGHTER_WIDTH \
        and fighter.y <= shot.y \
        and shot.y <= fighter.y + FIGHTER_HEIGHT:
            return True
        else:
            return False

    def did_fighter_shot_enemy(self, shot, enemy):
        if enemy.x <= shot.x \
        and shot.x <= enemy.x + ENEMY_WIDTH \
        and enemy.y <= shot.y \
        and shot.y <= enemy.y + ENEMY_HEIGHT:
            return True
        else:
            return False

    def did_enemy_hit_fighter(self, fighter, enemy):
        if (fighter.x <= enemy.x and enemy.x <= fighter.x + FIGHTER_WIDTH) \
        or (fighter.x <= enemy.x + ENEMY_WIDTH and enemy.x + ENEMY_WIDTH <= fighter.x + FIGHTER_WIDTH) \
        and enemy.y <= fighter.y \
        and fighter.y + FIGHTER_HEIGHT <= enemy.y:
            return True
        else:
            return False



    def enemy_hit_check(self, fighter, enemy_list, shot_list):
        for shot in shot_list:
            if shot.status == Status.Invalid:
                continue

            # 敵の攻撃結果チェック
            if type(shot) is EnemyShot:
                if self.did_enemy_shot_fighter(shot, fighter):
                    fighter.status = Status.Invalid

            # 戦闘機の攻撃結果チェック
            elif type(shot) is FighterShot:
                for enemy in enemy_list.enemy_group:
                    if self.did_fighter_shot_enemy(shot, enemy):
                        enemy.hp = enemy.hp - 1
                        shot.status = Status.Invalid
                        if enemy.hp == 0:
                            self.score = self.score + enemy.score

        # 戦闘機と敵の追突チェック・敵の侵入チェック
        for enemy in enemy_list.enemy_group:
            if self.did_enemy_hit_fighter(fighter, enemy) \
            or enemy.y == WINDOW_HEIGHT:
                fighter.status = Status.Invalid



    def enemy_atack(self, fighter, enemy_list):
        # 攻撃を行う敵を決定する処理
        distance_list = np.sort(np.unique(np.array([abs(enemy.x - fighter.x) for enemy in enemy_list.enemy_group])))
        if len(distance_list) >= 3:
            enemy_atack_distance_candidate = distance_list[0:3]
            enemy_atack_distance = np.random.choice(enemy_atack_distance_candidate, p = [0.55, 0.25, 0.2]) 
        elif len(distance_list) == 2:
            enemy_atack_distance_candidate = distance_list[0:2]
            enemy_atack_distance = np.random.choice(enemy_atack_distance_candidate, p = [0.6, 0.4])
        else:
            enemy_atack_distance = distance_list[0:1]

        enemy_atack_y_candidate = [enemy for enemy in enemy_list.enemy_group if abs(enemy.x - fighter.x) == enemy_atack_distance]
        enemy_atack_y = sorted(enemy_atack_y_candidate, key = lambda enemy: enemy.y, reverse = True)[0].y
        enemy_atack_list = [enemy for enemy in enemy_list.enemy_group if (abs(enemy.x - fighter.x) == enemy_atack_distance and enemy.y == enemy_atack_y)]

        # 攻撃処理
        [self.shot_list.append(EnemyShot(enemy_atack.x + ENEMY_WIDTH / 2, enemy_atack.y + ENEMY_HEIGHT, enemy_atack.shot_speed)) for enemy_atack in enemy_atack_list]


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

        # 敵の攻撃処理
        if pyxel.frame_count % 134 == 111:
            self.enemy_atack(self.fighter, self.enemy_list)

        # 敵・弾等の衝突判定
        self.enemy_hit_check(self.fighter, self.enemy_list, self.shot_list)

        # 敵の更新処理
        self.enemy_list.update()

        # 弾の更新処理
        if len(self.shot_list) > 0:
            [shot.update() for shot in self.shot_list]

        # 無効になった敵を削除する処理
        for enemy in self.enemy_list.enemy_group:
            if enemy.hp == 0 :
                self.enemy_list.enemy_group.remove(enemy)

        # 無効になった弾を削除する処理
        for shot in self.shot_list:
            if shot.status == Status.Invalid:
                self.shot_list.remove(shot)





    def draw(self):
        pyxel.cls(0)

        pyxel.text(10, 3, f'score = {self.score}', 2)

        self.fighter.draw()
        self.enemy_list.draw()

        if len(self.shot_list) > 0:
            [shot.draw() for shot in self.shot_list]

        if len(self.enemy_list.enemy_group) == 0:
            pyxel.text(WINDOW_WIDTH / 2 - 20, WINDOW_HEIGHT / 2 - 10 , 'Clear!!!', 6)

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

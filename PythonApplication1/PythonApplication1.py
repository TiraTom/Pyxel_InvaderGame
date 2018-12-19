import os
import pyxel
import random

class Ball:

	def __init__(self):
		self.x = 60
		self.y = 60
		self.r = 2

	def draw(self):
		pyxel.circ(self.x, self.y, self.r, 8)


class Wall:

	def __init__(self):
		self.x = 55
		self.y = 145
		self.height = 5
		self.width = 10
		self.color = 8

	def draw(self):
		pyxel.rect(self.x, self.y, self.height, self.width, self.color)

	def move_right(self):
		# 壁判定が必要
		self.x = self.x - 1
		pyxel.rect(self.x, self.y, self.height, self.width, self.color)

	def move_left(self):
		# 壁判定が必要
		self.x = self.x + 1
		pyxel.rect(self.x, self.y, self.height, self.width, self.color)



class Block:

	def __init__(self):
		self.block1 = [[(8 + 4 * i), 4, 2, 4, random.randint(0,15)] for i in range(26)]
		self.blocl2 = [[(4 + 4 * i), 8, 2, 4, random.randint(0,15)] for i in range(27)]
		self.blocl3 = [[(8 + 4 * i), 10, 2, 4, random.randint(0,15)] for i in range(26)]
		self.blocks = self.block1 + self.blocl2 + self.blocl3

	def draw(self):
		[pyxel.rect(block[0], block[1], block[0] + block[2], block[1] + block[3], block[4]) for block in self.blocks]



class App:
	def __init__(self):
		pyxel.init(120, 160, caption="BlockGame")

		#pyxel.load(f'{os.path.dirname(__file__)}/assets/block_game.pyxel')

		self.ball = Ball()
		self.wall = Wall()
		self.block = Block()

		pyxel.run(self.update, self.draw)


	def update(self):
		if pyxel.btnp(pyxel.KEY_Q):
			pyxel.quit()

	def draw(self):
		pyxel.cls(0)

		self.ball.draw()
		self.wall.draw()
		self.block.draw()

		pyxel.circ(60, 60, 2, 8)



App()






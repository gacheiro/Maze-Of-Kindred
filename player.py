import pygame
from timer import Timer
from sprite import Sprite
from loader import Loader
import common

class Player (Sprite):

	def __init__ (self, x, y):
		
		Sprite.__init__(self, x, y, 'princess')
		
		self.grid_x = x
		self.grid_y = y

		self.light = Sprite(x, y, 'light')
		self.light.offset_x = -96
		self.light.offset_y = -106
		self.light.play('default', loop=True)
		
		# walk timer
		self.timer = None
		
		# default orientation
		self.ori = 'up'
		
		# animations		
		self.add_anim('walk_up', common.WALK_MOVEMENT_TIME, range(0, 9))
		self.add_anim('walk_left', common.WALK_MOVEMENT_TIME, range(9, 18))
		self.add_anim('walk_down', common.WALK_MOVEMENT_TIME, range(18, 27))
		self.add_anim('walk_right', common.WALK_MOVEMENT_TIME, range(27, 36))
	
	@property
	def grid_x (self):		
		return int(self.x / common.TILE_SIZE)
		
	@property
	def grid_y (self):		
		return int(self.y / common.TILE_SIZE)
	
	@grid_x.setter
	def grid_x (self, x):		
		self.x = x * common.TILE_SIZE
		
	@grid_y.setter
	def grid_y (self, y):		
		self.y = y * common.TILE_SIZE
	
	def walk (self, x, y):
		
		assert(x == 1 or x == -1 or x == 0)
		assert(y == 1 or y == -1 or y == 0)
		
		if x == 0 and y == 0:
			return
		
		elif self.timer is None or self.timer.is_complete():
		
			x *= common.TILE_SIZE
			y *= common.TILE_SIZE
			
			self._prev_x = self.x
			self._prev_y = self.y
			
			self._next_x = self.x + x
			self._next_y = self.y + y
			
			self._move_x = x
			self._move_y = y
			
			if x < 0:
				self.ori = 'left'
			elif x > 0:
				self.ori = 'right'
			elif y > 0:
				self.ori = 'down'
			else:
				self.ori = 'up'

			self.play('walk_' + self.ori)
			self.timer = Timer(common.WALK_MOVEMENT_TIME)
	
	def update (self, time):
		
		Sprite.update(self, time)		
		self.light.update(time)
		
		if self.timer is not None and not self.timer.is_complete():

			self.timer.update(time)
			
			self.x = self._prev_x + self.timer.percent_done * self._move_x
			self.y = self._prev_y + self.timer.percent_done * self._move_y

		# adjust player light position
		self.light.x = self.x
		self.light.y = self.y
		

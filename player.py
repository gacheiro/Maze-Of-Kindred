import pygame
from animation import animation
from timer import timer
from sprite import sprite
from loader import loader
import common

class player (sprite):

	def __init__ (self, x, y):
		
		sprite.__init__(self, x, y, 'princess')
		
		self.x = x
		self.y = y
		self.light = sprite(x, y, 'light')
		self.light.play('default', loop=True)
		
		# walk timer
		self.timer = None
		
		# smooth walk utils
		self.__x = 0
		self.__y = 0
		self.offset_x = 0
		self.offset_y = 0
		self.__offset_x = 0
		self.__offset_y = 0
			
		# default orientation
		self.ori = 'up'
		
		# animations		
		self.add_anim('walk_up', common.WALK_MOVEMENT_TIME, range(0, 9))
		self.add_anim('walk_left', common.WALK_MOVEMENT_TIME, range(9, 18))
		self.add_anim('walk_down', common.WALK_MOVEMENT_TIME, range(18, 27))
		self.add_anim('walk_right', common.WALK_MOVEMENT_TIME, range(27, 36))
	
	def walk (self, x, y):
		
		assert(x == 1 or x == -1 or x == 0)
		assert(y == 1 or y == -1 or y == 0)
		
		if x == 0 and y == 0:
			return
		
		elif self.timer is None or self.timer.is_complete():
		
			self.x += x
			self.y += y
			
			self.__x = x
			self.__y = y
			
			self.__offset_x = common.TILE_SIZE * x
			self.__offset_y = common.TILE_SIZE * y
			
			if x < 0:
				self.ori = 'left'
			elif x > 0:
				self.ori = 'right'
			elif y > 0:
				self.ori = 'down'
			else:
				self.ori = 'up'

			self.play('walk_' + self.ori)
			self.timer = timer(common.WALK_MOVEMENT_TIME)
			
	def update (self, time):
		
		sprite.update(self, time)		
		self.light.update(time)
		
		if self.timer is not None and not self.timer.is_complete():
			self.timer.update(time)
			self.offset_x = self.__offset_x - float(self.timer.time_passed)/self.timer.time * self.__x * common.TILE_SIZE
			self.offset_y = self.__offset_y - float(self.timer.time_passed)/self.timer.time * self.__y * common.TILE_SIZE
			
			# normalize offset_x and offset_y
			if self.__x > 0 and self.offset_x < 0:
				self.offset_x = 0
			elif self.__x < 0 and self.offset_x > 0:
				self.offset_x = 0
			
			if self.__y > 0 and self.offset_y < 0:
				self.offset_y = 0
			elif self.__y < 0 and self.offset_y > 0:
				self.offset_y = 0
				
		else:
			self.offset_x = 0
			self.offset_y = 0
		
		# adjust player light position
		self.light.x = self.x * common.TILE_SIZE - self.offset_x - 112 + 16
		self.light.y = self.y * common.TILE_SIZE - self.offset_y - 112 + 16
			

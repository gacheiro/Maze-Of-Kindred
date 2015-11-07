import pygame
from animation import animation
from timer import timer
import common

WALK_MOVEMENT_TIME = 300

class player ():

	def __init__ (self, x, y):
	
		self.x = x
		self.y = y
		
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
		
		# sprite
		self.tileset = pygame.image.load('assets/opengameart/liberated pixel cup/princess.png')
		self.images = []
		for i in range (0, 4):
			for j in range (0, 9):
				self.images.append(self.tileset.subsurface(j * 64, i * 64, 64, 64))
		
		# animations
		self.up = animation(self.images[0:9])
		self.left = animation(self.images[10:18])
		self.down = animation(self.images[18:27])		
		self.right = animation(self.images[28:36])
	
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
				anim = self.left
			elif x > 0:
				self.ori = 'right'
				anim = self.right
			elif y > 0:
				self.ori = 'down'
				anim = self.down
			else:
				self.ori = 'up'
				anim = self.up
			
			anim.play(WALK_MOVEMENT_TIME)
			self.timer = timer(WALK_MOVEMENT_TIME)
			
	def update (self, time):
			
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
			
		anim = self.get_anim()
		anim.update(time)
		
	def get_anim (self):
	
		_r = None
		
		if self.ori == 'up':
			_r = self.up
		elif self.ori == 'left':
			_r = self.left
		elif self.ori == 'right':
			_r = self.right
		else:
			_r = self.down
			
		return _r	
	
	def get_image (self):
	
		return self.get_anim().get_image()
		

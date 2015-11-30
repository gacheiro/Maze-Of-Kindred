import pygame
from animation import Animation
from loader import Loader

class Sprite (pygame.sprite.Sprite):

	def __init__ (self, x, y, key):
	
		pygame.sprite.Sprite.__init__(self)
		
		self.x = x
		self.y = y
		
		self.key = key
		self.frames = Loader.get(key)
		self.anims = {}
		self.current_anim = 'default'
		self.anims['default'] = Animation(1000, self.frames)
		self.image = self.anims[self.current_anim].get_image()	
		
		self.rect = self.image.get_rect() 
		self.rect.x = x
		self.rect.y = y

	def add_anim (self, name, duration, frames):
		
		__frames = []
		for f in frames:
			__frames.append(self.frames[f])
		
		a = Animation(duration, __frames)
		self.anims[name] = a
		
		return a
	
	def play (self, name, loop=False):
		
		a = self.anims[name]
		a.play(loop)
		
		self.current_anim = name
		
		return a
		
	def update (self, time):
		
		self.anims[self.current_anim].update(time)
		self.image = self.anims[self.current_anim].get_image()
		
	def get_anim (self, name=None):
	
		if name is None:
			name = self.current_anim
			
		return self.anims[name]


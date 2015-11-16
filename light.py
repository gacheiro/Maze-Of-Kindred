import pygame
from animation import animation
from random import shuffle
import common

class light ():

	def __init__ (self, x, y):
		
		self.x = x
		self.y = y
		
		self.image = pygame.image.load('assets/foundtimegames/dither_circle.png').convert_alpha()
		self.frames = []
		for i in range (0, 5):
			self.frames.append(self.image.subsurface(i * 224, 0, 224, 224))
		shuffle(self.frames)
		
		self.anim = animation(common.TORCH_ANIMATION_TIME, self.frames)
		
	def get_image (self):
	
		return self.anim.get_image()
		

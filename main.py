import pygame
from maze import maze
from player import player
from timer import timer
from random import shuffle
from random import randint
from sprite import sprite
from loader import loader
import common

class maze_of_kindred ():

	def __init__ (self, width, height, tile_size):
		
		self.width = width
		self.height = height
		self.tile_size = tile_size
		
		self.player = None
		self.maze = None
		
		self.enable_graphics = common.ENABLE_GRAPHICS
		self.enable_sound = common.ENABLE_SOUND

		self.fade_timer = None
		
		self.castle = None
		self.torches = None
		self.lights = None
		
	def load (self):
		
		pygame.display.set_caption('Maze of Kindred')
		
		self.screen = pygame.display.set_mode((common.GAME_WIDTH, common.GAME_HEIGHT))
		self.screen.convert_alpha()
		
		loader.image('assets/opengameart/liberated pixel cup/castle.png', 'castle')
		loader.image('assets/opengameart/nathanLovatoArt/sound.png', 'sound')
		loader.image('assets/opengameart/nathanLovatoArt/no_sound.png', 'nosound')
		loader.image('assets/opengameart/nathanLovatoArt/restart.png', 'restart')
		
		loader.tileset('assets/opengameart/liberated pixel cup/princess.png', 'princess', 4, 9, 64, 64)
		loader.tileset('assets/opengameart/liberated pixel cup/torch.png', 'torch', 1, 9, 48, 48)
		loader.tileset('assets/opengameart/liberated pixel cup/flame.png', 'flame', 1, 12, 24, 36)
		loader.tileset('assets/foundtimegames/dither_circle.png', 'light', 1, 5, 224, 224)
		loader.tileset('assets/opengameart/liberated pixel cup/cement.png', 'maze_cement', 6, 3, 32, 32)
		loader.tileset('assets/opengameart/liberated pixel cup/castlefloors_outside.png', 'maze_floor', 5, 4, 32, 32)
		
		loader.audio('assets/opengameart/tozan/longbust.ogg', 'music')
		
	def create (self):
		
		self.player = player(self.width/2,  self.height - 2)
		self.maze = maze(self.width, self.height, self.tile_size)
		self.maze.create()
		
		self.music = loader.get('music')
		self.music.play(-1)
		
		if self.enable_sound:
			self.music.set_volume(0.2)
			
		else:
			self.music.set_volume(0)

		# black screen fade out
		self.fade_timer = timer(2000)
		
		self.castle = sprite(0, -16, 'castle')
		
		self.torches = []
		self.torches.append(sprite(336, 80, 'torch'))
		self.torches.append(sprite(480, 80, 'torch'))
		self.torches.append(sprite(83, 140, 'flame'))
		
		self.lights = []
		self.lights.append(sprite(240, 0, 'light'))
		self.lights.append(sprite(384, 0, 'light'))
		self.lights.append(sprite(-13, 58, 'light'))
		
		for t in self.torches:
			t.play('default', loop=True)
			
		for l in self.lights:
			l.play('default', loop=True)
		
		self.sound = sprite(common.GAME_WIDTH - 80, 10, 'sound')
		self.nosound = sprite(common.GAME_WIDTH - 80, 14, 'nosound')
		self.restart = sprite(common.GAME_WIDTH - 70, 15, 'restart')
		
		self.fog = pygame.Surface((self.maze.image.get_width(), self.maze.image.get_height()))
		self.fog.set_colorkey((255, 0, 255))
		
	def draw (self):
		
		surface = self.maze.image.copy()
		self.fog.fill((0, 0, 0))
		
		x = common.GAME_WIDTH * 0.5 - self.player.x * self.tile_size - 16 + self.player.offset_x
		y = common.GAME_HEIGHT * 0.8 - self.player.y * self.tile_size + self.player.offset_y

		# normalize x and y
		if x > 0: x = 0
		elif x < -320: x = -320
		
		if y > 0: y = 0
		elif y < -960: y = -960
		
		# player visual x and y
		player_x = self.player.x * common.TILE_SIZE - self.player.offset_x - 16
		player_y = self.player.y * common.TILE_SIZE - self.player.offset_y - 32
		
		surface.blit(self.castle.image, (self.castle.x, self.castle.y))
		surface.blit(self.player.image, (player_x, player_y))
		
		for t in self.torches:
			surface.blit(t.image, (t.x, t.y))
		
		for l in self.lights:
			self.fog.blit(l.image, (l.x, l.y))
		
		player_light = self.player.light
		self.fog.blit(player_light.image, (player_light.x, player_light.y))

		self.screen.blit(surface, (x, y))
		
		if common.ENABLE_FOG:
			self.screen.blit(self.fog, (x, y))
		
		if not self.fade_timer.is_complete():
		
			alpha = 255 - float(self.fade_timer.time_passed) / self.fade_timer.time * 255 
			alpha = int(alpha)
			
			fog = pygame.Surface((common.GAME_WIDTH, common.GAME_HEIGHT), pygame.SRCALPHA)
			pygame.draw.rect(fog, (0, 0, 0, alpha), (0, 0, common.GAME_WIDTH, common.GAME_HEIGHT))
			self.screen.blit(fog, (0, 0))
			
		elif self.is_at_door():
		
			fog = pygame.Surface((common.GAME_WIDTH, common.GAME_HEIGHT), pygame.SRCALPHA)
			pygame.draw.rect(fog, (0, 0, 0, 170), (0, 0, common.GAME_WIDTH, common.GAME_HEIGHT))
			self.screen.blit(fog, (0, 0))
			
			self.screen.blit(self.restart.image, (self.restart.x, self.restart.y))

		elif self.enable_sound:	
			self.screen.blit(self.sound.image, (self.sound.x, self.sound.y))
			
		else:
			self.screen.blit(self.nosound.image, (self.nosound.x, self.nosound.y))
		
		pygame.display.update()
		
	def main (self):
		
			clock = pygame.time.Clock()
			
			pygame.key.set_repeat(1, 100)
			
			x = y = 0
			
			while True:
				
				time = clock.tick(60)
				
				self.fade_timer.update(time)
				
				for event in pygame.event.get():
					
					if event.type == pygame.QUIT:
						pygame.quit()
						return
						
					elif event.type == pygame.MOUSEBUTTONUP:
						
						if self.sound.rect.collidepoint(event.pos):
							
							if self.is_at_door(): # clicking on restart button
								self.create()
								
							else: # clicking on enable/disable sound
								self.enable_sound = not self.enable_sound
							
						if self.enable_sound:
							self.music.set_volume(0.2)
						else:
							self.music.set_volume(0)
							
					elif event.type == pygame.KEYDOWN and not self.is_at_door():
						
						if event.key == pygame.K_LEFT or event.key == pygame.K_a:
							x = -1; y = 0
							
						elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
							x = 1; y = 0
							
						elif event.key == pygame.K_UP or event.key == pygame.K_w:
							y = -1; x = 0
							
						elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
							y = 1; x = 0
					
					elif event.type == pygame.KEYUP or self.is_at_door():
						x = y = 0
				
					if self.maze.matrix[self.player.y + y][self.player.x + x] == 0:
						self.player.walk(x, y)	
					
				self.player.update(time)
				
				for t in self.torches:
					t.update(time)
					
				for l in self.lights:
					l.update(time)
					
				self.draw()
				
			#	print self.player.x, self.player.y
				print clock.get_fps()
		
	def is_at_door (self):
		
		return self.player.x == 13 and self.player.y == 6

if __name__ == '__main__':
	
	pygame.init()
	pygame.mixer.init()
	
	m = maze_of_kindred(common.MAZE_WIDTH, common.MAZE_HEIGHT, common.TILE_SIZE)
	m.load()
	m.create()
	m.main()

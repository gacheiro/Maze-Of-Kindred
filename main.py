import pygame
from maze import maze
from player import player
from timer import timer
from random import shuffle
from random import randint
from sprite import sprite
import common

class maze_of_kindred ():

	def __init__ (self, width, height, tile_size):
		
		self.width = width
		self.height = height
		self.tile_size = tile_size
		
		self.player = player(width/2, height - 2)
		
		self.enable_graphics = common.ENABLE_GRAPHICS
		self.enable_sound = common.ENABLE_SOUND
		
		self.maze = maze(width, height, tile_size)
		
		self.fade_timer = None
		
		self.castle = None
		self.torches = None
		self.lights = None
		
	def load (self):
		
		pygame.display.set_caption('Maze of Kindred')
		
		self.screen = pygame.display.set_mode((common.GAME_WIDTH, common.GAME_HEIGHT))
		self.screen.convert_alpha()
		
		self.maze.load()
		
		self.castle_image = pygame.image.load('assets/opengameart/liberated pixel cup/castle.png').convert_alpha()
		self.b_sound = pygame.image.load('assets/opengameart/nathanLovatoArt/sound.png').convert_alpha()
		self.b_nosound = pygame.image.load('assets/opengameart/nathanLovatoArt/no_sound.png').convert_alpha()
		self.b_restart = pygame.image.load('assets/opengameart/nathanLovatoArt/restart.png').convert_alpha()

		torch = pygame.image.load('assets/opengameart/liberated pixel cup/torch.png').convert_alpha()
		flame = pygame.image.load('assets/opengameart/liberated pixel cup/flames.png').convert_alpha()
		light = pygame.image.load('assets/foundtimegames/dither_circle.png').convert_alpha()
		
		# split images into frames
		self.torch_frames = []
		for i in range (0, 9):
			self.torch_frames.append(torch.subsurface(48 * i, 0, 48, 48))
		
		self.flame_frames = []
		for i in range (0, 12):
			self.flame_frames.append(flame.subsurface(24 * i, 0, 24, 36))
		
		self.light_frames = []
		for i in range (0, 5):
			self.light_frames.append(light.subsurface(i * 224, 0, 224, 224))
			
		pygame.mixer.music.load('assets/opengameart/tozan/longbust.ogg')
		
	def create (self):
		
		self.maze.create()
		
		pygame.mixer.music.play(-1)
		
		if self.enable_sound:
			pygame.mixer.music.set_volume(0.2)
		else:
			pygame.mixer.music.set_volume(0)
			
		self.player.x = self.width/2
		self.player.y = self.height - 2
		
		# black screen fade out
		self.fade_timer = timer(2000)
		
		self.castle = sprite(0, -16, self.castle_image)
		
		self.torches = []
		self.torches.append(sprite(336, 80, self.torch_frames[:]))
		self.torches.append(sprite(480, 80, self.torch_frames[:]))
		self.torches.append(sprite(83, 138, self.flame_frames[:]))
		
		self.lights = []
		self.lights.append(sprite(0, 0, self.light_frames[:]))
		self.lights.append(sprite(240, 0, self.light_frames[:]))
		self.lights.append(sprite(384, 0, self.light_frames[:]))
		self.lights.append(sprite(-13, 58, self.light_frames[:]))
		
		for t in self.torches:
			t.play('default', loop=True)
			shuffle(t.get_anim().frames)
			
		for l in self.lights:
			l.play('default', loop=True)
			shuffle(l.get_anim().frames)
		
		self.sound = sprite(common.GAME_WIDTH - 80, 10, self.b_sound)
		self.nosound = sprite(common.GAME_WIDTH - 80, 14, self.b_nosound)
		self.restart = sprite(common.GAME_WIDTH - 70, 15, self.b_restart)
		
	def draw (self):
		
		surface = self.maze.surface.copy()
		fog = pygame.Surface((surface.get_width(), surface.get_height()))
		fog.set_colorkey((255, 0, 255))
		
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
			fog.blit(l.image, (l.x, l.y))

		self.screen.blit(surface, (x, y))
		
		if common.ENABLE_FOG:
			self.screen.blit(fog, (x, y))
		
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
							pygame.mixer.music.set_volume(0.2)
						else:
							pygame.mixer.music.set_volume(0)
							
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
				
				self.lights[0].x = self.player.x * common.TILE_SIZE - self.player.offset_x - 112 + 16
				self.lights[0].y = self.player.y * common.TILE_SIZE - self.player.offset_y - 112 + 16
				
				for t in self.torches:
					t.update(time)
					
				for l in self.lights:
					l.update(time)
					
				self.draw()
				
			#	print self.player.x, self.player.y
			#	print clock.get_fps()
		
	def is_at_door (self):
		
		return self.player.x == 13 and self.player.y == 6

if __name__ == '__main__':
	
	pygame.init()
	pygame.mixer.init()
	
	m = maze_of_kindred(common.MAZE_WIDTH, common.MAZE_HEIGHT, common.TILE_SIZE)
	m.load()
	m.create()
	m.main()

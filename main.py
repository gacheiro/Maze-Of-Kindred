import pygame
from maze import maze
from player import player
from timer import timer
from animation import animation
from random import shuffle
from light import light
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
		self.b_rect = None
		
		self.torches = []
		self.lights = []
		
	def load (self):
		
		pygame.display.set_caption('Maze of Kindred')
		
		self.screen = pygame.display.set_mode((common.GAME_WIDTH, common.GAME_HEIGHT))
		self.screen.convert_alpha()
		
		self.maze.load()
		
		self.castle = pygame.image.load('assets/opengameart/liberated pixel cup/castle.png').convert_alpha()
		self.b_sound = pygame.image.load('assets/opengameart/nathanLovatoArt/sound.png').convert_alpha()
		self.b_nosound = pygame.image.load('assets/opengameart/nathanLovatoArt/no_sound.png').convert_alpha()
		self.b_restart = pygame.image.load('assets/opengameart/nathanLovatoArt/restart.png').convert_alpha()
		
		# button sound and restart click rect
		self.b_rect = self.b_sound.get_rect(topleft=(common.GAME_WIDTH - 80, 10))
		
		# torches and flames (sprite animation)
		torch = pygame.image.load('assets/opengameart/liberated pixel cup/torch.png').convert_alpha()
		flame = pygame.image.load('assets/opengameart/liberated pixel cup/flames.png').convert_alpha()
		
		self.torch_images = []
		for i in range (0, 9):
			self.torch_images.append(torch.subsurface(48 * i, 0, 48, 48))
			
		self.torches.append(animation(self.torch_images)) # torch 1
		torch_images_copy = self.torch_images[:] # copy images
		shuffle(torch_images_copy) 	# then shuffle
		self.torches.append(animation(torch_images_copy)) # torch 2
		
		self.flame_images = []
		for i in range (0, 12):
			self.flame_images.append(flame.subsurface(24 * i, 0, 24, 36))
		self.torches.append(animation(self.flame_images))
		
		self.torches_pos = [
			(336, 80),
			(480, 80),
			(83, 138),
		]
		
		# lights are the vision of the player
		self.lights.append(light(0, 0))
		self.lights.append(light(240, 0))
		self.lights.append(light(384, 0))
		self.lights.append(light(-13, 58))
		
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
		
		for t in self.torches:
			t.play(common.TORCH_ANIMATION_TIME, loop=True)
			
		for l in self.lights:
			l.anim.play(common.TORCH_ANIMATION_TIME, loop=True)
			
		self.fog = self.maze.surface.copy()
		
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
		
		surface.blit(self.castle, (0, -16))
		surface.blit(self.player.get_image(), (player_x, player_y))
		
		for i in range (0, len(self.torches)): # torches sprite animations
			surface.blit(self.torches[i].get_image(), self.torches_pos[i])
		
		for l in self.lights: # the vision of the player
			fog.blit(l.get_image(), (l.x, l.y))

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
			
			self.screen.blit(self.b_restart, (common.GAME_WIDTH - 70, 15))

		elif self.enable_sound:	
			self.screen.blit(self.b_sound, (common.GAME_WIDTH - 80, 10))
			
		else:
			self.screen.blit(self.b_nosound, (common.GAME_WIDTH - 80, 14))
		
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
						
						if self.b_rect.collidepoint(event.pos):
							
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
					l.anim.update(time)
					
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

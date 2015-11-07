import pygame
from maze import maze
from player import player
from timer import timer
import common

class maze_of_kindred ():

	def __init__ (self, width, height, tile_size):
		
		self.width = width
		self.height = height
		self.tile_size = tile_size
		
	#	self.player = player(width/2, height - 2)
		self.player = player(13, 6)
		
		self.enable_graphics = common.ENABLE_GRAPHICS
		self.enable_sound = common.ENABLE_SOUND
		
		self.maze = maze(width, height, tile_size)
		
		self.fade_timer = None
		self.b_rect = None
		
	def load (self):
		
		pygame.display.set_caption('Maze of Kindred')
		
		self.screen = pygame.display.set_mode((common.GAME_WIDTH, common.GAME_HEIGHT))
		self.screen.convert_alpha()
		
		self.maze.load()
		
		self.castle = pygame.image.load('assets/opengameart/liberated pixel cup/castle.png').convert_alpha()
		self.b_sound = pygame.image.load('assets/opengameart/nathanLovatoArt/sound.png').convert_alpha()
		self.b_nosound = pygame.image.load('assets/opengameart/nathanLovatoArt/no_sound.png').convert_alpha()
		self.b_restart = pygame.image.load('assets/opengameart/nathanLovatoArt/restart.png').convert_alpha()
		
		# button click point
		self.b_rect = self.b_sound.get_rect(topleft=(common.GAME_WIDTH - 80, 10))
		
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
		
		self.fade_timer = timer(2000)
		
	def draw (self):
		
		surface = self.maze.surface.copy()
		
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
		
		self.screen.fill((0, 0, 0))
		surface.blit(self.castle, (0, -16))
		surface.blit(self.player.get_image(), (player_x, player_y))
		
		self.screen.blit(surface, (x, y))
		
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
					
						x = y = 0
						
						if event.key == pygame.K_LEFT or event.key == pygame.K_a:
							x -= 1
							
						elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
							x += 1
							
						elif event.key == pygame.K_UP or event.key == pygame.K_w:
							y -= 1
							
						elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
							y += 1
							
						if self.maze.matrix[self.player.y + y][self.player.x + x] == 0:
							self.player.walk(x, y)
				
				self.player.update(time)				
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

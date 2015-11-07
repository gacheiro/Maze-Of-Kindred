from random import randint
import common
import pygame

# this code is a adaptation of Emanuele Feronato's maze generator
# checkout http://www.emanueleferonato.com/2015/06/30/pure-javascript-perfect-tile-maze-generation-with-a-bit-of-magic-thanks-to-phaser/
# for original code

class maze ():

	def __init__ (self, width, height, tile_size):
	
		self.matrix = None
		self.graphics = None
		
		self.width = width
		self.height = height
		self.tile_size = tile_size
	
	def load (self):
	
		self.cement_tileset = pygame.image.load('assets/opengameart/liberated pixel cup/cement.png').convert()		
		self.floor = pygame.image.load('assets/opengameart/liberated pixel cup/castlefloors_outside.png').convert()
		
		self.cement_images = [
			self.cement_tileset.subsurface(32, 128, 32, 32),
			self.cement_tileset.subsurface(32, 96, 32, 32),
			self.cement_tileset.subsurface(0, 160, 32, 32),
			self.cement_tileset.subsurface(32, 160, 32, 32),
			self.floor.subsurface(32, 0, 32, 32),
			self.floor.subsurface(64, 128, 32, 32),
			self.floor.subsurface(0, 32, 32, 32),
		]
		
		self.surface = pygame.Surface((self.width * self.tile_size, self.height * self.tile_size), pygame.SRCALPHA)
	
	def create (self):
		
		wall_base_image_id = 0
		wall_image_id = 1
		floor_image_id = 6
		
		self.matrix = []
		self.graphics = []
		
		for i in range (0, self.height):
			self.matrix.append([])
			self.graphics.append([])
			for j in range (0, self.width):
				self.matrix[i].append(1)
				self.graphics[i].append(floor_image_id)
			
		posX = self.height - 3
		posY = self.width/2
		
		self.matrix[posX][posY] = 0
		moves = []
		moves.append(posY + posX * self.width)
		
		while len(moves) > 0:
		
			possibleDirections = ""
			
			if posX + 3 > 0 and posX + 3 < self.height - 1 and self.matrix[posX + 3][posY] == 1:
				possibleDirections += 'S'
				
			if posX - 3 > 0 and posX - 3 < self.height - 1 and self.matrix[posX - 3][posY] == 1:
				possibleDirections += 'N'
			
			if posY - 2 > 0 and posY - 2 < self.width - 1 and self.matrix[posX][posY - 2] == 1:
				possibleDirections += 'W'
			
			if posY + 2 > 0 and posY + 2 < self.width - 1 and self.matrix[posX][posY + 2] == 1:
				possibleDirections += 'E'
			
			if len(possibleDirections) > 0:
			
				move = randint(0, len(possibleDirections) - 1)
				
				if possibleDirections[move] == 'N':
					
					self.matrix[posX - 3][posY] = 0
					self.matrix[posX - 2][posY] = 0
					self.matrix[posX - 1][posY] = 0
					posX -= 3
				
				elif possibleDirections[move] == 'S':
				
					self.matrix[posX + 3][posY] = 0
					self.matrix[posX + 2][posY] = 0
					self.matrix[posX + 1][posY] = 0
					posX += 3
					
				elif possibleDirections[move] == 'W':

					self.matrix[posX][posY - 2] = 0
					self.matrix[posX][posY - 1] = 0
					posY -= 2
					
				elif possibleDirections[move] == 'E':
				
					self.matrix[posX][posY + 2] = 0
					self.matrix[posX][posY + 1] = 0
					posY += 2
			
				moves.append(posY + posX * self.width)
				
			else:			
				back = moves.pop(-1)
				posX = int(back / self.width)
				posY = back % self.width
		
		# erase lines (walls) in castle area and beginning area
		for i in range (0, 11):
			for j in range (1, self.width - 1):
				
				_i = min(i, 1)
				self.matrix[i][j] = 0
				self.matrix[-_i - 2][j] = 0
					
		# build graphics
		for i in range (0, self.height - 1):
			for j in range (0, self.width):
			
				if self.matrix[i][j] == 1:
					if self.matrix[i+1][j] == 1:
						self.graphics[i][j] = wall_image_id
					else:
						self.graphics[i][j] = wall_base_image_id
						
		# last line border
		for j in range (0, self.width):
			self.graphics[self.height - 1][j] = 1
			
		# upper border
		for j in range (1, self.width - 1):
			self.matrix[6][j] = 1
			
		self.matrix[6][0] = 0
		self.matrix[6][-1] = 0
		self.matrix[6][13] = 0
		self.matrix[7][2] = 1
		self.matrix[7][3] = 1
		
		# graphics are static so just draw once onto the surface
		self.draw(self.surface)
		
	def draw (self, surface):
		
	#	if common.ENABLE_GRAPHICS:
			
			for i in range (0, self.height):
				for j in range (0, self.width):				
					
					id = self.graphics[i][j]
					
					if id == 0 or id == 1:
						surface.blit(self.cement_images[id], (j * self.tile_size, i * self.tile_size))
						
						# draws borders over the for better appearance
						
						border_color = (58, 49, 48)						
						
						if j + 1 < self.width and self.matrix[i][j+1] == 0:
							pygame.draw.line(surface, border_color, (j * self.tile_size + 31, i * self.tile_size), (j * self.tile_size + 31, i * self.tile_size + 32), 1)
						
						if j - 1 >= 0 and self.matrix[i][j-1] == 0:
							pygame.draw.line(surface, border_color, (j * self.tile_size, i * self.tile_size), (j * self.tile_size, i * self.tile_size + 31), 1)
						
						if i - 1 >= 0 and self.matrix[i-1][j] == 0:
							pygame.draw.line(surface, border_color, (j * self.tile_size, i * self.tile_size), (j * self.tile_size + 31, i * self.tile_size), 1)
						
					else:
						surface.blit(self.cement_images[id], (j * self.tile_size, i * self.tile_size))
					
	#	else:
	#		
	#		for i in range (0, self.height):
	#			for j in range (0, self.width):
	#				if self.matrix[i][j] == 0:
	#					rect = pygame.Rect(j * self.tile_size, i * self.tile_size, self.tile_size, self.tile_size)
	#					pygame.draw.rect(surface, (255, 255, 255), rect)

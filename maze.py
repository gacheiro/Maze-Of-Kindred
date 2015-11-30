from random import randint
import common
import pygame
from loader import Loader

# this code is a adaptation of Emanuele Feronato's maze generator
# checkout http://www.emanueleferonato.com/2015/06/30/pure-javascript-perfect-tile-maze-generation-with-a-bit-of-magic-thanks-to-phaser/
# for original code

class Maze ():

	def __init__ (self, width, height, tile_size):
	
		self.matrix = None
		self.graphics = None
		
		self.width = width
		self.height = height
		self.tile_size = tile_size
	
		self.image = pygame.Surface((self.width * self.tile_size, self.height * self.tile_size))
		
	def create (self):
		
		cement = Loader.get('maze_cement') # cement tiles
		floor = Loader.get('maze_floor')   # floor tiles
		CEMENT_BASE_WALL = 0
		CEMENT_TOP_WALL = 1
		
		self.tiles = [
			cement[13], # CEMENT_BASE_WALL
			cement[10], # CEMMENT_TOP_WALL
			floor[13],  # FLOOR
			floor[14],
			floor[17],
			floor[18],
		]
		
		self.matrix = []
		self.graphics = []
		
		for i in range (0, self.height):
			self.matrix.append([])
			self.graphics.append([])
			for j in range (0, self.width):
				self.matrix[i].append(1)
				self.graphics[i].append(randint(2, 4))
			
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
						self.graphics[i][j] = CEMENT_TOP_WALL
					else:
						self.graphics[i][j] = CEMENT_BASE_WALL
						
		# last line border
		for j in range (0, self.width):
			self.graphics[self.height - 1][j] = 1
			
		# upper border
		for j in range (1, self.width - 1):
			self.matrix[6][j] = 1
			
		self.matrix[6][0] = 0
		self.matrix[6][-1] = 0
		self.matrix[6][13] = 0
		
		self.__draw()
		Loader.set(self.image, 'maze')
		
		self.matrix[7][2] = 1
		self.matrix[7][3] = 1
		
	def __draw (self):
		
		for i in range (0, self.height):
			for j in range (0, self.width):				
				
				id = self.graphics[i][j]
				
				if self.matrix[i][j] == 1: # if is wall then
				
					# draws borders over the walls for better appearance
					self.image.blit(self.tiles[id], (j * self.tile_size, i * self.tile_size))
					
					border_color = (58, 49, 48)						
					
					if j + 1 < self.width and self.matrix[i][j+1] == 0:
						pygame.draw.line(self.image, border_color, (j * self.tile_size + 31, i * self.tile_size), (j * self.tile_size + 31, i * self.tile_size + 32), 1)
					
					if j - 1 >= 0 and self.matrix[i][j-1] == 0:
						pygame.draw.line(self.image, border_color, (j * self.tile_size, i * self.tile_size), (j * self.tile_size, i * self.tile_size + 31), 1)
					
					if i - 1 >= 0 and self.matrix[i-1][j] == 0:
						pygame.draw.line(self.image, border_color, (j * self.tile_size, i * self.tile_size), (j * self.tile_size + 31, i * self.tile_size), 1)
					
				else:
					self.image.blit(self.tiles[id], (j * self.tile_size, i * self.tile_size))
					

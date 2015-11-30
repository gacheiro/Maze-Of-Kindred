import pygame

class Loader ():

	cache = {}
	
	def __init__ (self):
		pass
	
	@classmethod
	def image (cls, path, key):
	
		img = pygame.image.load(path).convert_alpha()
		cls.cache[key] = img
		
		return img
	
	@classmethod
	def tileset (cls, path, key, rows, columns, tile_width, tile_height):
	
		img = pygame.image.load(path).convert_alpha()
		
		tiles = []
		for i in range (0, rows):
			for j in range (0, columns):
				tiles.append(img.subsurface(j * tile_width, i * tile_height, tile_width, tile_height))
				
		cls.cache[key] = tiles
		
		return tiles
	
	@classmethod	
	def audio (cls, path, key):
	
		aud = pygame.mixer.Sound(path)
		cls.cache[key] = aud
		
		return aud
		
	@classmethod
	def get (cls, key):
	
		return cls.cache[key]
		
	@classmethod
	def set (cls, data, key):
	
		cls.cache[key] = data
		

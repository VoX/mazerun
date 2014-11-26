import pygame

class Wall(pygame.sprite.Sprite):
	# WALL
	
	def __init__(self, x, y, width, height, color):
	
		# call parent
		super(Wall, self).__init__()
		
		# make blue wall
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
		
		# set location
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
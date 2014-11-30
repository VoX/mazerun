import pygame

class Wall(pygame.sprite.Sprite):
	# WALL
	
	def __init__(self, left, top):
	
		# call parent
		super(Wall, self).__init__()
		
		# make blue wall
		self.image = pygame.Surface((35, 35))
		self.image.fill((255,255,255))
		
		# set location
		self.rect = self.image.get_rect()
		self.rect.top = top
		self.rect.left = left
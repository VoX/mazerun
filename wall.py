import pygame
from constants import *

class Wall(pygame.sprite.Sprite):
	# WALL
	
	def __init__(self, left, top):
	
		# call parent
		super(Wall, self).__init__()
		
		# make blue wall
		self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
		self.image.fill((BRN))
		
		# set location
		self.rect = self.image.get_rect()
		self.rect.top = top
		self.rect.left = left
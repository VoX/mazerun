import pygame

class Room(object):
	# base room class
	
	# each room has a list of walls
	wall_list = None
	enemy_sprites = None
	
	def __init__(self):
		self.wall_list = pygame.sprite.Group()
		self.enemy_sprites = pygame.sprite.Group()
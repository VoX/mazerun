import pygame, random

class Room(object):
	# base room class
	
	# each room has a list of walls
	wall_list = None
	enemy_list = None
	enemy_sprites = None
	enemy_count = random.randint(1,30)
	
	def __init__(self):
		self.wall_list = pygame.sprite.Group()
		self.enemy_list = pygame.sprite.Group()
		self.treasure_list = pygame.sprite.Group()
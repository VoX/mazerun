import pygame
from constants import *
		
class Player(pygame.sprite.Sprite):
	# player controlled thing
	
	# set speed vector
	change_x = 0
	change_y = 0
	
	def __init__(self, x, y):
		
		# call parent
		super(Player, self).__init__()
		
		# set height/width
		self.image = pygame.Surface([15, 15])
		self.image.fill(WHT)
		
		# set location
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
		
	def change_speed(self, x, y):
		# change player speed, called with keypress
		self.change_x += x
		self.change_y += y
		
	def move(self, walls):
		# find new player position
		
		# move left/right
		self.rect.x += self.change_x
		
		# horizontal collision?
		block_hit_list = pygame.sprite.spritecollide(self, walls, False)
		for block in block_hit_list:
			# if moving right, set our right side to the left side of
			# collided object
			if self.change_x > 0:
				self.rect.right = block.rect.left
			else:
				# if moving left, do opposite
				self.rect.left = block.rect.right
				
		# move up/down
		self.rect.y += self.change_y
		
		# vertical collision?
		block_hit_list = pygame.sprite.spritecollide(self, walls, False)
		for block in block_hit_list:
			# if moving down, set our bottom side to the top side of
			# collided object
			if self.change_y > 0:
				self.rect.bottom = block.rect.top
			else:
				# if moving up, do opposite
				self.rect.top = block.rect.bottom
import pygame
from constants import *
import random

class Enemy(pygame.sprite.Sprite):
	# base enemy class

	# set speed
	change_x = 0
	change_y = 0

	def __init__(self):
		
		# call parent
		super(Monster, self).__init__()
		
		# set height/width
		self.image = pygame.image.load('slime.png')
		
		# set location
		self.rect = self.image.get_rect()
		self.health = 30
		self.counter = 0
		
	def change_speed(self, x, y):
		# change enemy speed, called with keypress
		self.change_x += x
		self.change_y += y
		
	def move(self, walls):
		# find new enemy position

		if self.counter < 60:
			self.counter += 1
		else:
			self.change_x = random.randint(-1,1)
			self.change_y = random.randint(-1,1)
		
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

	def take_damage(self, damage, incoming_x, incoming_y):
		self.damage = damage
		self.health -= self.damage
		self.incoming_x = incoming_x
		self.incoming_y = incoming_y
		self.change_x = self.rect.x - self.incoming_x
		self.change_y = self.rect.y - self.incoming_y
import pygame
from constants import *
import random
from util.perlin import SimplexNoise

perlin = SimplexNoise(period=500)
		
class Player(pygame.sprite.Sprite):
	# player controlled thing
	
	# set speed vector
	change_x = 0
	change_y = 0
	
	def __init__(self, health, x, y):
		
		# call parent
		super(Player, self).__init__()
		
		# set height/width
		self.image = pygame.image.load(IMG_DIR + 'new dude.png')
		
		# set location
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
		self.health = health
		self.gold = 0
		self.inventory = []

	@property
	def hp(self):
		return self.health

	@property
	def ranged_damage(self):
		return 10

	@property
	def melee_damage(self):
		return 15
		
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

	def take_damage(self, damage, incoming_x, incoming_y):
		self.damage = damage
		self.health -= self.damage
		self.incoming_x = incoming_x
		self.incoming_y = incoming_y
		self.counter = 0
		if (self.rect.x - self.incoming_x) < 0:
			self.rect.move(self.damage, 0)
		elif (self.rect.x - self.incoming_x) > 0:
			self.rect.move(-self.damage, 0)
		if (self.rect.y - self.incoming_y) < 0:
			self.rect.move(0,self.damage)
		elif (self.rect.y - self.incoming_y) > 0:
			self.rect.move(0, -self.damage)

	def add_loot(self, treasure):
		if treasure.type == 'coins':
			count = int(treasure.count)
			self.gold += count
		else:
			self.inventory.append(treasure)
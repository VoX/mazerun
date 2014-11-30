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

		# set stats
		self.level = 1
		self.stats = {
				'Strength': 1,
				'Attack': 5,
				'Defense': 5,
				'Agility': 1,
				'Intellect': 1,
				'EXP': 0
		}
		self.class_type = {
				'Warrior': 0,
				'Archer': 0,
				'Wizard': 0
		}
		self.current_hp = 100
		#self.main_stat = self.find_main_stat(self.class_type)
		self.name = 'Rougelicker'
		self.equipped = {}
		
		for treasure in EQUIPMENT_TYPES:
			self.equipped[treasure] = None
			
	@property
	def max_hp(self):
		return (100 + ((self.level-1)*5) + (self.class_type['Warrior']*5))

	@property
	def ranged_damage(self):
		return 10

	@property
	def melee_damage(self):
		return 15
		
	@property
	def max_mp(self):
		return (0 + (self.class_type['Wizard']*10))
		
	@property
	def defense(self):
		return (self.stats['Defense'] + self.armor() + self.class_type['Archer'])
		
	@property
	def strength(self):
		return (self.stats['Strength'] + (self.class_type['Warrior']*2))
		
	@property
	def agility(self):
		return (self.stats['Agility'] + (self.class_type['Archer']*2))
		
	@property
	def intellect(self):
		return (self.stats['Intellect'] + (self.class_type['Wizard']*2))
		
	@property
	def EXP(self):
		return self.stats['EXP']
		
	def armor(self):
		armor = 0
		for slot in self.equipped.keys():
			if self.equipped[slot]:
				try:
					armor += self.equipped[slot].armor
				except AttributeError:
					pass
		return armor
		
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
		self.current_hp -= self.damage
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
		if treasure.item_type == 'coins':
			count = int(treasure.count)
			self.gold += count
		else:
			self.inventory.append(treasure)
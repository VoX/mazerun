import pygame, random
from util.perlin import SimplexNoise
from constants import *
from treasure import Treasure

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
		self.equipped = {}

		for treasure in EQUIPMENT_TYPES:
			self.equipped[treasure] = None

		# set stats
		self.level = 1
		self.class_type = {
				'Warrior': 0,
				'Archer': 0,
				'Wizard': 0
		}
		self.stats = {
				'M. Damage': self.melee_damage,
				'R. Damage': self.ranged_damage(),
				'Strength': self.strength,
				'Agility': self.agility,
				'Intellect': self.intellect,
				'EXP': 0
		}
		
		self.current_hp = 100
		#self.main_stat = self.find_main_stat(self.class_type)
		self.name = 'Rougelicker'
		
		### FIX THIS, need to separate loot (location on the map) and
		### Treasure (the item itself)
		#self.equipped['m. weapon'] = 
			
	@property
	def max_hp(self):
		return (100 + ((self.level-1)*5) + (self.class_type['Warrior']*5))

	@property
	def max_mp(self):
		return (0 + (self.class_type['Wizard']*10))
		
	#@property
	#def defense(self):
	#	return (5 + self.armor() + self.class_type['Archer'])
		
	@property
	def strength(self):
		stren = 0
		for slot in self.equipped.keys():
			if self.equipped[slot] != None:
				stren += self.equipped[slot].str_buff

		return (1 + stren + (self.class_type['Warrior']*2))
		
	@property
	def agility(self):
		agi = 0
		for slot in self.equipped.keys():
			if self.equipped[slot] != None:
				agi += self.equipped[slot].agi_buff

		return (1 + agi + (self.class_type['Archer']*2))
		
	@property
	def intellect(self):
		intel = 0
		for slot in self.equipped.keys():
			if self.equipped[slot] != None:
				stren += self.equipped[slot].aint_buff

		return (1 + intel + (self.class_type['Wizard']*3))
		
	@property
	def EXP(self):
		return self.stats['EXP']

	def ranged_damage(self):
		r_dam = 0
		for slot in self.equipped.keys():
			if self.equipped[slot]:
				try:
					r_dam += self.equipped[slot].r_damage
				except AttributeError:
					pass

		r_dam += (3+(self.agility*2))
					
		return r_dam


	def melee_damage(self):
		m_dam = 0
		for slot in self.equipped.keys():
			if self.equipped[slot]:
				try:
					m_dam += self.equipped[slot].m_damage
				except AttributeError:
					pass 
		
		m_dam += (5+(self.strength*2))

		return m_dam
		
	def armor(self):
		armor = 0
		for slot in self.equipped.keys():
			if self.equipped[slot]:
				try:
					armor += self.equipped[slot].armor
				except AttributeError:
					pass
		return armor

	def earn_EXP(self, EXP):
		self.stats['EXP'] += EXP

	def equip_item(self, item):
		self.equipped[item.item_type] = item
		
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
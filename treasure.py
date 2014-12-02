import pygame, random
from constants import *

class Treasure(pygame.sprite.Sprite):
	# treasure class, for money too

	def __init__(self, x, y, title='Nada', desc='', item_type='trash', armor=0,
				m_damage=0, r_damage=0, str_buff=0, agi_buff=0, int_buff=0):
		super(Treasure, self).__init__()
		
		self.title = title
		self.desc = desc
		self.armor = armor
		self.str_buff = str_buff
		self.agi_buff = agi_buff
		self.int_buff = int_buff
		self.get_type()
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y

	def get_type(self):
		choice = random.randint(0,100)
		if choice < 20:
			self.item_type = 'coins'
			x = random.randint(1,30)
			self.count = x
			self.image = self.coin_image(self.count)			
		elif choice < 40:
			self.item_type = 'M. Weapon'
			self.title = 'Greatsword'
			self.m_damage = 5
			self.agi_buff = -1
			self.image = pygame.image.load(IMG_DIR + 'swadia.png')
		elif choice < 60:
			self.item_type = 'Hat'
			self.title = 'Iron Helm'
			self.armor = 2
			self.agi_buff = -1
			self.int_buff = -1
			self.image = pygame.image.load(IMG_DIR + 'helm.png')
		elif choice < 80:
			self.item_type = 'Hat'
			self.title = 'Fool\'s Crown'
			self.str_buff = 1
			self.int_buff = -1
			self.image = pygame.image.load(IMG_DIR + 'crown.png')
		elif choice <= 100:
			self.item_type = 'R. Weapon'
			self.title = 'Apprentice Wand'
			self.r_damage = 4
			self.str_buff = -1
			self.int_buff = 1
			self.image = pygame.image.load(IMG_DIR + 'wand.png')

	def coin_image(self, c):
		if c > 15:
			return pygame.image.load(IMG_DIR + 'gold_tiny.png')
		elif c < 50:
			return pygame.image.load(IMG_DIR + 'gold_small.png')
import pygame, random
from constants import *

class Treasure(pygame.sprite.Sprite):
	# treasure class, for money too

	def __init__(self, x, y, title='Nada', desc='', item_type='trash', armor=0, buff=0, attack=0):
		super(Treasure, self).__init__()
		
		self.title = title
		self.desc = desc
		self.get_type()
		self.armor = armor
		self.buff = buff
		self.attack = attack
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
			self.item_type = 'weapon'
			self.title = 'greatsword'
			self.image = pygame.image.load(IMG_DIR + 'swadia.png')
		elif choice < 60:
			self.item_type = 'shirt'
			self.title = 'iron helm'
			self.image = pygame.image.load(IMG_DIR + 'helm.png')
		elif choice < 80:
			self.item_type = 'hat'
			self.title = 'fool\'s crown'
			self.image = pygame.image.load(IMG_DIR + 'crown.png')
		elif choice <= 100:
			self.item_type = 'weapon'
			self.title = 'apprentice wand'
			self.image = pygame.image.load(IMG_DIR + 'wand.png')

	def coin_image(self, c):
		if c > 15:
			return pygame.image.load(IMG_DIR + 'gold_tiny.png')
		elif c < 50:
			return pygame.image.load(IMG_DIR + 'gold_small.png')
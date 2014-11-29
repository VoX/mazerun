import pygame, random
from constants import *

class Treasure(pygame.sprite.Sprite):
	# treasure class, for money too

	def __init__(self, x, y):
		super(Treasure, self).__init__()

		self.get_type()
		if self.type == 'coins':
			self.count = self.get_count()
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y

	def get_type(self):
		choice = random.randint(0,100)
		if choice < 20:
			self.type = 'coins'
			self.image = pygame.image.load(IMG_DIR + 'gold.png')
		elif choice < 40:
			self.type = 'weapon'
			self.image = pygame.image.load(IMG_DIR + 'swadia.png')
		elif choice < 60:
			self.type = 'armor'
			self.image = pygame.image.load(IMG_DIR + 'helm.png')
		elif choice < 80:
			self.type = 'accessory'
			self.image = pygame.image.load(IMG_DIR + 'crown.png')
		elif choice <= 100:
			self.type = 'magic'
			self.image = pygame.image.load(IMG_DIR + 'wand.png')

	def get_count(self):
		x = random.randint(1,30)
		return x
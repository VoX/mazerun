import pygame

from constants import *

class EXPReward(pygame.sprite.Sprite):
	def __init__(self, x, y, reward):
		
		# call parent
		super(EXPReward, self).__init__()
		
		# set height/width
		self.image = self.get_image(reward)
		
		# set location
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
		self.counter = 50

	def get_image(self, reward):
		if reward == 25:
			return pygame.image.load(IMG_DIR + '25EXP.png')
		if reward == 50:
			return pygame.image.load(IMG_DIR + '50EXP.png')
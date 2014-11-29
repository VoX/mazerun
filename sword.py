import pygame
import random
from constants import *

class Sword(pygame.sprite.Sprite):
	# swadia
	def __init__(self, shape, x, y):
		# call parent
		super(Sword, self).__init__()

		self.shape = shape
		self.image = self.get_shape(self.shape)

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def get_shape(self, shape):
		if shape == 'up':
			return pygame.image.load(IMG_DIR + 'swadia.png')
		if shape == 'left':
			return pygame.image.load(IMG_DIR + 'swadia left.png')
		if shape == 'right':
			return pygame.image.load(IMG_DIR + 'swadia right.png')
		if shape == 'down':
			return pygame.image.load(IMG_DIR + 'swadia down.png')
		
	def swing(self, x_speed, y_speed):
		self.x_speed = x_speed
		self.y_speed = y_speed
		if self.x_speed > 0:
			pass
		if self.x_speed < 0:
			self.rect.x -= 40
		if self.y_speed > 0:
			self.rect.y -= 40
		if self.y_speed < 0:
			pass
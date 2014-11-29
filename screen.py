import pygame
from constants import *
from pygame.locals import *

class Screen(object):

	def __init__(self):
		self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
		pygame.display.set_caption('ROUGELICK')

	def to_screen(self, to_draw):
		to_draw.draw(self.screen)
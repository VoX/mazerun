import pygame
from constants import *
from pygame.locals import *

class Screen(object):

	def __init__(self):
		self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
		pygame.display.set_caption('ROUGELICK')
		self.font = pygame.font.SysFont(None, 48)
		self.small_font = pygame.font.SysFont(None, 20)
		self.inventory_screen = self.small_font.render('Inventory', True, WHT, BLK)
		self.equipment_screen = self.small_font.render('Equipment', True, WHT, BLK)
		self.stats_screen = self.small_font.render('ARGH', True, WHT, BLK)
		#self.draw_inventory()
		#self.draw_equipment()
		pygame.display.flip()

	def to_screen(self, to_draw):
		to_draw.draw(self.screen)
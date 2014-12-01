import pygame
from constants import *
from pygame.locals import *

class Screen(object):

	def __init__(self):
		self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
		pygame.display.set_caption('ROUGELICK')
		self.font = pygame.font.SysFont(None, 48)
		self.small_font = pygame.font.SysFont(None, 20)
		self.gold_screen = self.small_font.render('Gold: ', True, WHT, BLK)
		self.inventory_screen = self.small_font.render('Inventory', True, WHT, BLK)
		self.equipment_screen = self.small_font.render('Equipment', True, WHT, BLK)
		self.stats_screen = self.small_font.render('ARGH', True, WHT, BLK)
		self.draw_inventory()
		self.draw_equipment()
		pygame.display.flip()

	def to_screen(self, to_draw):
		to_draw.draw(self.screen)

	def draw_alert(self, alert, color=WHT):
		# draws alert box
		self.alert = self.font.render('xxx', True, BLK, BLK)
		self.screen.blit(self.alert, (0, 790))
		try:
			pygame.display.flip()
		except:
			pass
		self.alert = self.font.render(alert, True, color, BLK)
		self.screen.blit(self.alert, (0, 790))
		pygame.display.flip()
		
	def draw_stats(self, player_stats, color=WHT):
		# renders player stats
		self.screen.blit(self.stats_screen, (750, 0))
		self.stats_screen = self.small_font.render(player_stats.name, True, color, BLK)
		self.screen.blit(self.stats_screen, (750, 0))
		self.stats_screen = self.small_font.render('Level: {}'.format(player_stats.level), True, color, BLK)
		self.screen.blit(self.stats_screen, (750, 15))
		self.stats_screen = self.small_font.render('EXP: {}'.format(player_stats.EXP), True, color, BLK)
		self.screen.blit(self.stats_screen, (750, 30))
		self.stats_screen = self.small_font.render('HP: {}/{}'.format((player_stats.current_hp), (player_stats.max_hp)), True, color, BLK)
		self.screen.blit(self.stats_screen, (750, 45))
		line = 60
		for stat in STATS:
			if hasattr(player_stats, stat):
				s = str(getattr(player_stats, stat))
			else:
				s = str(player_stats.stats[stat])
				
				self.stats_screen = self.small_font.render('{}: {}'.format(stat, s), True, color, BLK)
				self.screen.blit(self.stats_screen, (750, line))
				line += 15
		self.stats_screen = self.small_font.render('Armor: {}'.format(player_stats.armor()), True, color, BLK)
		self.screen.blit(self.stats_screen, (750, line))
		
	def draw_gold(self, gold_count):
		# renders gold
		self.screen.blit(self.gold_screen, (750, 385))
		self.gold = self.small_font.render(str(gold_count), True, WHT, BLK)
		self.screen.blit(self.gold, (800, 385))
		
	def draw_inventory(self, inventory=None):
		# renders inventory
		self.screen.blit(self.inventory_screen, (750, 400))
		if inventory:
			items = inventory.get_items()
		else:
			items = []
		for i in range(items.__len__()):
			line = self.small_font.render('xxx', True, BLK, BLK)
			self.screen.blit(line, (750, ((i+1)*15)+400))
		for item in items:
			line = self.small_font.render(item.title, True, WHT, BLK)
			self.screen.blit(line, (750, (items.index(item)+1)*15+400))
		
	def draw_equipment(self, equipment=START_EQUIPMENT):
		# renders equipment. will change for more awesomeness
		self.screen.blit(self.equipment_screen, (750, 200))
		for i in range(equipment.keys().__len__()):
			line = self.small_font.render('xxx', True, BLK, BLK)
			self.screen.blit(line, (750, ((i+1)*15)+200))
		i = 1
		for slot in EQUIPMENT_TYPES:
			try:
				line_text = slot+': '+equipment[slot].title
			except:
				line_text = slot+': '
			line = self.small_font.render(line_text, True, WHT, BLK)
			self.screen.blit(line, (750, i*15+200))
			i += 1
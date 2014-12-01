from constants import *
import operator

class Inventory(object):
	# player inventory
	
	def __init__(self):
		# sets up initial blank inventory
		self.inventory = {}
		
	def get_items(self):
		return self.inventory.keys()
		
	def add_to_inventory(self, item, player):
		# adds item to inventory
		if item.item_type == 'trash':
			return
		elif item.item_type == 'coins':
			player.gold += item.count
			return
		if player.equipped[item.item_type]:
			try:
				self.inventory[item] += 1
			except:
				self.inventory[item] = 1
		else:
			player.equip_item(item)
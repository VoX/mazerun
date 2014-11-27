import pygame, random
from room import Room
from wall import Wall
from enemy import Enemy
from constants import *

class Room1(Room):
	def __init__(self):
		Room.__init__(self)
		# make the walls (x_pos, y_pos, width, height)
		
		# This is a list of walls. Each is in the form [x, y, width, height]
		walls = [[0, 0, 20, 250, WHT],
				[0, 350, 20, 250, WHT],
				[780, 0, 20, 250, WHT],
				[780, 350, 20, 250, WHT],
				[20, 0, 760, 20, WHT],
				[20, 580, 760, 20, WHT],
				[390, 50, 20, 500, BLU]
				]
		# loop through walls list
		for item in walls:
			wall = Wall(item[0], item[1], item[2], item[3], item[4])
			self.wall_list.add(wall)
			
class Room2(Room):
	def __init__(self):
		Room.__init__(self)
		# make the walls (x_pos, y_pos, width, height)
		
		# This is a list of walls. Each is in the form [x, y, width, height]
		walls = [[0, 0, 20, 250, RED],
				[0, 350, 20, 250, RED],
				[780, 0, 20, 250, RED],
				[780, 350, 20, 250, RED],
				[20, 0, 760, 20, RED],
				[20, 580, 760, 20, RED],
				[190, 50, 20, 500, GRN],
				[590, 50, 20, 500, GRN]
				]
		# loop through walls list
		for item in walls:
			wall = Wall(item[0], item[1], item[2], item[3], item[4])
			self.wall_list.add(wall)
			
class Room3(Room):
	def __init__(self):
		Room.__init__(self)
		
		walls = [[0, 0, 20, 250, PUR],
				[0, 350, 20, 250, PUR],
				[780, 0, 20, 250, PUR],
				[780, 350, 20, 250, PUR],
				[20, 0, 760, 20, PUR],
				[20, 580, 760, 20, PUR]
				]
				
		# loop through walls list
		for item in walls:
			wall = Wall(item[0], item[1], item[2], item[3], item[4])
			self.wall_list.add(wall)
			
		for x in xrange(100, 800, 100):
			for y in xrange(50, 451, 300):
				wall = Wall(x, y, 20, 200, RED)
				self.wall_list.add(wall)
				
		for x in xrange(150, 700, 100):
			wall = Wall(x, 200, 20, 200, WHT)
			self.wall_list.add(wall)
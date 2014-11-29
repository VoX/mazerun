import pygame, constants
from room import Room
from individual_rooms import *

class GameMap(object):
	# map, for storing room objects and their attribs

	def get_rooms(self):
		rooms = []
	
		room = Room1()
		rooms.append(room)
	
		room = Room2()
		rooms.append(room)
	
		room = Room3()
		rooms.append(room)
		return rooms
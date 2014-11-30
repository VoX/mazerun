import pygame, constants
from room import Room
from individual_rooms import *

class GameMap(object):
	# map, for storing room objects and their attribs

	def get_rooms(self):
		rooms = []
	
		room = Room()
		rooms.append(room)
	
		room = Room()
		rooms.append(room)
	
		room = Room()
		rooms.append(room)
		return rooms
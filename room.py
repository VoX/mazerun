import pygame, random
from constants import *
from random import randint, choice
from enemy import Enemy
from treasure import Treasure
from wall import Wall

class Room(object):
	# base room class
	
	# each room has a list of walls
	wall_list = None
	enemy_list = None
	enemy_sprites = None
	enemy_count = random.randint(1,30)
	
	def __init__(self):
		self.walls = self.get_blank_map()
		self.treasure = self.get_blank_map()
		self.enemy = self.get_blank_map()
		self.floor = self.get_blank_map()
		self.wall_list = pygame.sprite.Group()
		self.enemy_list = pygame.sprite.Group()
		self.treasure_list = pygame.sprite.Group()
		self.chamber_list = []
		
		self.get_chambers()
		self.connect_chambers()
		
		for t in xrange(TREASURES):
			while 1:
				col = randint(0, COLUMNS-1)
				row = randint(0, ROWS-1)
				treasure = Treasure((row*TILE_SIZE),(col*TILE_SIZE))
				if not self.walls[row][col] and self.floor[row][col]:
					self.treasure[row][col] = treasure
					self.treasure_list.add(treasure)
					break
		
		for m in xrange(ENEMIES):
			while 1:
				col = randint(0, COLUMNS-1)
				row = randint(0, ROWS-1)
				enemy = Enemy()
				enemy.rect.left = row*TILE_SIZE
				enemy.rect.top = col*TILE_SIZE
				if not self.treasure[row][col] and self.floor[row][col]:
					self.enemy[row][col] = enemy
					self.enemy_list.add(enemy)
					break
			
		self.fill_map()
		
	def fill_map(self):
		for i in range(ROWS):
			for j in range(COLUMNS):
				wall = Wall(i*TILE_SIZE, j*TILE_SIZE)
				if not self.floor[i][j]:
					self.walls[i][j] = wall
					self.wall_list.add(wall)
					
	def get_chambers(self):
		# set initial room
		chamber = self.check_chamber(coord=(0,0), height=5, length=5)
		self.chamber_list.append(chamber)
		chambers = 1
		keep_going = 50
		while chambers <= MAX_CHAMBERS and keep_going:
			height = randint(4, 10)
			length = randint(4, 10)
			x = randint(0, COLUMNS-1)
			y = randint(0, ROWS)
			chamber = self.check_chamber(coord=(x,y), height=height, length=length)
			if chamber:
				chambers += 1
				self.chamber_list.append(chamber)
			else:
				keep_going -= 1
				
		for chamber in self.chamber_list:
			self.make_random_door(chamber)
			
	def connect_chambers(self):
		for chamber in self.chamber_list:
			i = self.chamber_list.index(chamber)
			try:
				next = self.chamber_list[i+1]
			except:
				next = self.chamber_list[0]
			if chamber.door[0] < next.door[0]:
				start = chamber.door[0]
				end = next.door[0]
			else:
				start = next.door[0]
				end = chamber.door[0]
			for x in xrange(start, end):
				self.walls[x][chamber.door[1]] = 0
				for w in self.wall_list:
					if w.rect.left == x*TILE_SIZE and w.rect.top == chamber.door[1]*TILE_SIZE:
						self.wall_list.remove(w)
				self.floor[x][chamber.door[1]] = 1
			if chamber.door[1] < next.door[1]:
				start = chamber.door[1]
				end = next.door[1]
			else:
				start = next.door[1]
				end = chamber.door[1]
			for y in xrange(start, end):
				self.walls[next.door[0]][y] = 0
				for w in self.wall_list:
					if w.rect.left == next.door[0]*TILE_SIZE and w.rect.top == y*TILE_SIZE:
						self.wall_list.remove(w)
				self.floor[next.door[0]][y] = 1
				
	def check_chamber(self, coord, height, length):
		for i in xrange(0, height):
			for j in xrange(0, length):
				if coord[1]+i > COLUMNS-1:
					return False
				if coord[0]+j > ROWS-1:
					return False
				if self.floor[coord[0]+j][coord[1]+i]:
					return False
		chamber = Chamber(start=coord, height=height, length=length)
		self.create_chamber(chamber)
		return chamber
		
	def create_chamber(self, chamber):
		# make top and bottom walls
		for i in xrange(0, chamber.length):
			# syntactic sugar
			fst = chamber.start[0]+i
			snd = chamber.start[1]
			wall = Wall(fst*TILE_SIZE, snd*TILE_SIZE)
			self.walls[fst][snd] = 1
			self.wall_list.add(wall)
			
			fst = chamber.start[0]+i
			snd = chamber.start[1]+chamber.height-1
			wall = Wall(fst*TILE_SIZE, snd*TILE_SIZE)
			self.walls[fst][snd] = 1
			self.wall_list.add(wall)
		# make side walls
		for i in xrange(0, chamber.height):
			fst = chamber.start[0]
			snd = chamber.start[1]+i
			wall = Wall(fst*TILE_SIZE, snd*TILE_SIZE)
			self.walls[fst][snd] = 1
			self.wall_list.add(wall)
			
			fst = chamber.start[0]+chamber.length-1
			snd = chamber.start[1]+i
			wall = Wall(fst*TILE_SIZE, snd*TILE_SIZE)
			self.walls[fst][snd] = 1
			self.wall_list.add(wall)
			
		# fill in floor
		for x in xrange(1, chamber.length-1):
			for y in range(1, chamber.height-1):
				self.floor[chamber.start[0]+x][chamber.start[1]+y] = 1
				
	def make_random_door(self, chamber):
		while 1:
			dir = choice(DIRECTIONS)
			if dir in ['north','south']:
				block = randint(1, chamber.length-2)
			else:
				block = randint(1, chamber.height-2)
			if dir == 'north':
				coord = (chamber.start[0]+block, chamber.start[1])
				check = (coord[0], coord[1]-1)
				next = (coord[0], coord[1]-2)
			if dir == 'south':
				coord = (chamber.start[0]+block, chamber.start[1]+chamber.height-1)
				check = (coord[0], coord[1]+1)
				next = (coord[0], coord[1]+1)
			if dir == 'east':
				coord = (chamber.start[0], chamber.start[1]+block)
				check = (coord[0]-1, coord[1])
				next = (coord[0]-2, coord[1])
			if dir == 'west':
				coord = (chamber.start[0]+chamber.length-1, chamber.start[1]+block)
				check = (coord[0]+1, coord[1])
				next = (coord[0]+2, coord[1])
			door = self.check_door(coord, check, next)
			if door:
				self.walls[coord[0]][coord[1]] = 0
				for w in self.wall_list:
					if w.rect.left == coord[0]*TILE_SIZE and w.rect.top == coord[1]*TILE_SIZE:
						self.wall_list.remove(w)
				self.floor[coord[0]][coord[1]] = 2
				chamber.door = (coord[0], coord[1])
				return
				
	def check_door(self, coord, check, next):
		# is it at bounds?
		if check[0] < 0 or check[1] < 0:
			return False
		# is it next to wall?
		try:
			if self.walls[check[0]][check[1]]:
				# is that wall next to another wall?
				if self.walls[next[0]][next[1]]:
					return False
				else:
					try:
						self.walls[check[0]][check[1]] = 0
						for w in self.wall_list:
							if w.rect.left == coord[0]*TILE_SIZE and w.rect.top == coord[1]*TILE_SIZE:
								self.wall_list.remove(w)
					except:
						pass # sometimes it will be one away from border
		except:
			return False
		return True
		
	def get_blank_map(self):
		# returns 2d list with all values set to 0\
		maplist = []
		for i in xrange(ROWS):
			row = []
			for j in range(COLUMNS):
				row.append(0)
			maplist.append(row)
		return maplist
		
	def is_block_empty(self, row, col):
		if not self.treasure[row][col] and not self.monsters[row][col] and not self.walls[row][col]\
		and not (self.player[0]/TILE_SIZE, self.player[1]/TILE_SIZE) == (row, col):
			return True
		else:
			return False
			
	def has_wall(self, row, col):
		row = row/TILE_SIZE
		col = col/TILE_SIZE
		if self.walls[row][col]:
			return True
		else:
			return False
			
class Chamber(object):
	
	def __init__(self, height=5, length=5, start=(0,0)):
		self.title = 'Generic room'
		self.start = start
		self.length = length
		self.height = height
		self.end = (self.start[0]+self.length, self.start[1]+self.length)
		self.door = []
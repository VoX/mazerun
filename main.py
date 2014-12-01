import pygame, math, sys, random
from pygame.locals import *

sys.path.append('roguey\classes')

from constants import *
from treasure import Treasure
from gamemap import GameMap
from player import Player
from enemy import Enemy
from inventory import Inventory
from game import Game

def main():
	while 1:
		pygame.init()
		game = Game()

if __name__ == '__main__':
	main()

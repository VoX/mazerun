# init colors
BLK = (0,0,0)
BRN = (83,51,3)
GRY = (130,140,135)
WHT = (255,255,255)
BLU = (0,0,255)
GRN = (0,255,0)
RED = (255,0,0)
PUR = (255,0,255)

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
ROWS = 20
COLUMNS = 21
MAX_CHAMBERS = 7

EQUIPMENT_TYPES = ('Hat', 'Torso', 'Legs', 'Feet', 'Back', 'Neck', 'Hands', 'M. Weapon', 'R. Weapon')
START_EQUIPMENT = {}
for treasure in EQUIPMENT_TYPES:
	if treasure == 'M. Weapon':
		START_EQUIPMENT[treasure] = 'Greatsword'
	elif treasure == 'R. Weapon':
		START_EQUIPMENT[treasure] = 'Longbow'
	else:
		START_EQUIPMENT[treasure] = None
	
STATS = ('Strength', 'Agility', 'Intellect')
CLASS = ('Warrior', 'Archer', 'Wizard')

DIRECTIONS = ['north','south','east','west']

TILE_SIZE = 35

ENEMIES = 40
TREASURES = 3

IMG_DIR = 'res/'
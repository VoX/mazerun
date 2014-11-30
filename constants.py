# init colors
BLK = (0,0,0)
GRY = (130,140,135)
WHT = (255,255,255)
BLU = (0,0,255)
GRN = (0,255,0)
RED = (255,0,0)
PUR = (255,0,255)

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
ROWS = 21
COLUMNS = 20
MAX_CHAMBERS = 7

EQUIPMENT_TYPES = ('hat', 'shirt', 'pants', 'shoes', 'back', 'neck', 'hands', 'weapon')
START_EQUIPMENT = {}
for treasure in EQUIPMENT_TYPES:
	START_EQUIPMENT[treasure] = None
	
STATS = ('Strength', 'Attack', 'Defense', 'Agility', 'Intellect', 'EXP')
CLASS = ('Warrior', 'Archer', 'Wizard')

DIRECTIONS = ['north','south','east','west']

TILE_SIZE = 35

ENEMIES = 40
TREASURES = 3

IMG_DIR = 'res/'
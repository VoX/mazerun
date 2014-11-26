import pygame
import wall
from constants import *
from room import Room
from individual_rooms import *
from player import Player

def main():
	## MAIN GAME LOOP ##
	
	# init pygame
	pygame.init()
	screen = pygame.display.set_mode([800, 600])
	pygame.display.set_caption('ROUGELICK')
	clock = pygame.time.Clock()
	
	# create player paddle
	player = Player(50, 50)
	moving_sprites = pygame.sprite.Group()
	moving_sprites.add(player)
	
	# create rooms
	# there has to be a better way
	rooms = []
	
	room = Room1()
	rooms.append(room)
	
	room = Room2()
	rooms.append(room)
	
	room = Room3()
	rooms.append(room)
	
	current_room_num = 0
	current_room = rooms[current_room_num]
		
	done = False
	
	while not done:
		# event processing
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					done = True
				if event.key == pygame.K_LEFT:
					player.change_speed(-5, 0)
				if event.key == pygame.K_RIGHT:
					player.change_speed(5, 0)
				if event.key == pygame.K_UP:
					player.change_speed(0, -5)
				if event.key == pygame.K_DOWN:
					player.change_speed(0, 5)
			
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					player.change_speed(5, 0)
				if event.key == pygame.K_RIGHT:
					player.change_speed(-5, 0)
				if event.key == pygame.K_UP:
					player.change_speed(0, 5)
				if event.key == pygame.K_DOWN:
					player.change_speed(0, -5)
					
		# game logic
		
		player.move(current_room.wall_list)
		
		if player.rect.x < -15:
			if current_room_num == 0:
				current_room_num = 2
				current_room = rooms[current_room_num]
				player.rect.x = 790
			elif current_room_num == 2:
				current_room_num = 1
				current_room = rooms[current_room_num]
				player.rect.x = 790
			else:
				current_room_num = 0
				current_room = rooms[current_room_num]
				player.rect.x = 790
				
		if player.rect.x > 801:
			if current_room_num == 0:
				current_room_num = 1
				current_room = rooms[current_room_num]
				player.rect.x = 0
			elif current_room_num == 1:
				current_room_num = 2
				current_room = rooms[current_room_num]
				player.rect.x = 0
			else:
				current_room_num = 0
				current_room = rooms[current_room_num]
				player.rect.x = 0
				
		# drawing (move to screen.py next)
		screen.fill(BLK)
		
		moving_sprites.draw(screen)
		current_room.wall_list.draw(screen)
		
		pygame.display.flip()
		
		clock.tick(60)
		
	pygame.quit()
	
if __name__ == "__main__":
	main()
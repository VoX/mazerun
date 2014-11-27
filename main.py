import pygame
import wall
from constants import *
from room import Room
from individual_rooms import *
from player import Player
from bullet import Bullet
from sword import Sword

def main():
	## MAIN GAME LOOP ##
	
	# init pygame
	pygame.init()
	screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
	pygame.display.set_caption('ROUGELICK')
	clock = pygame.time.Clock()
	
	# create player paddle
	player = Player(50, 50)
	all_sprites = pygame.sprite.Group()
	moving_sprites = pygame.sprite.Group()
	bullet_list = pygame.sprite.Group()
	sword_list = pygame.sprite.Group()
	weapon_type = 'ranged'

	all_sprites.add(player)
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
	for i in xrange(MAX_ENEMY):
		enemy = Enemy()
		enemy.rect.x = random.randrange(SCREEN_WIDTH)
		enemy.rect.y = random.randrange(SCREEN_HEIGHT)
		roll = random.randint(0,100)
		if roll > 34:
			rooms[0].enemy_list.add(enemy)
		elif roll > 67:
			rooms[1].enemy_list.add(enemy)
		else:
			rooms[2].enemy_list.add(enemy)

	all_sprites.add(current_room.enemy_list)
		
	done = False
	
	while not done:
		# event processing
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					done = True
				if event.key == pygame.K_LCTRL:
						if weapon_type == 'ranged':
							weapon_type = 'melee'
						else:
							weapon_type = 'ranged'
				if event.key == pygame.K_LEFT:
					player.change_speed(-5, 0)
				if event.key == pygame.K_RIGHT:
					player.change_speed(5, 0)
				if event.key == pygame.K_UP:
					player.change_speed(0, -5)
				if event.key == pygame.K_DOWN:
					player.change_speed(0, 5)
				if weapon_type == 'ranged':
					if event.key == pygame.K_w:
						bullet = Bullet('tall',player.rect.centerx,player.rect.centery-10)
						bullet.fire(0,1)
						all_sprites.add(bullet)
						bullet_list.add(bullet)
					elif event.key == pygame.K_a:
						bullet = Bullet('long',player.rect.centerx-10,player.rect.centery)
						bullet.fire(-1,0)
						all_sprites.add(bullet)
						bullet_list.add(bullet)
					elif event.key == pygame.K_s:
						bullet = Bullet('tall',player.rect.centerx,player.rect.centery)
						bullet.fire(0,-1)
						all_sprites.add(bullet)
						bullet_list.add(bullet)
					elif event.key == pygame.K_d:
						bullet = Bullet('long',player.rect.centerx,player.rect.centery)
						bullet.fire(1,0)
						all_sprites.add(bullet)
						bullet_list.add(bullet)
				if weapon_type == 'melee':
					if event.key == pygame.K_w:
						sword = Sword('tall',player.rect.centerx,player.rect.centery)
						sword.swing(0,1)
						all_sprites.add(sword)
						sword_list.add(sword)
					elif event.key == pygame.K_a:
						sword = Sword('long',player.rect.centerx,player.rect.centery)
						sword.swing(-1,0)
						all_sprites.add(sword)
						sword_list.add(sword)
					elif event.key == pygame.K_s:
						sword = Sword('tall',player.rect.centerx,player.rect.centery)
						sword.swing(0,-1)
						all_sprites.add(sword)
						sword_list.add(sword)
					elif event.key == pygame.K_d:
						sword = Sword('long',player.rect.centerx,player.rect.centery)
						sword.swing(1,0)
						all_sprites.add(sword)
						sword_list.add(sword)
					
			
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
			# cleanup bullets on room-change
			# there must be a better way to do this
			for b in bullet_list:
				bullet_list.remove(b)
				all_sprites.remove(b)
			# room change logic
			if current_room_num == 0:
				current_room_num = 2
				current_room = rooms[current_room_num]
				player.rect.x = 790
				
			elif current_room_num == 2:
				player.rect.x = 790
				current_room_num = 1
				current_room = rooms[current_room_num]
				
			else:
				current_room_num = 0
				current_room = rooms[current_room_num]
				player.rect.x = 790
				
		if player.rect.x > 801:
			# cleanup bullets on room-change
			# there must be a better way to do this
			for b in bullet_list:
				bullet_list.remove(b)
				all_sprites.remove(b)
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

		for b in bullet_list:

			# collision?
			b.move()
			block_hit_list = pygame.sprite.spritecollide(b, current_room.wall_list, False)
			enemy_hit_list = pygame.sprite.spritecollide(b, current_room.enemy_list, False)

			# remove bullet
			for block in block_hit_list:
				bullet_list.remove(b)
				all_sprites.remove(b)

			for enemy in enemy_hit_list:
				bullet_list.remove(b)
				all_sprites.remove(b)
				# deal damage
				enemy.take_damage(player.ranged_damage, player.rect.x, player.rect.y)
				if enemy.health <= 0:
					current_room.enemy_list.remove(enemy)
					all_sprites.remove(enemy)

			# remove bullet if off screen
				
		for s in sword_list:

			# collision?
			enemy_hit_list = pygame.sprite.spritecollide(s, current_room.enemy_list, False)

			for enemy in enemy_hit_list:
				# deal damage
				enemy.take_damage(player.melee_damage, player.rect.x, player.rect.y)
				if enemy.health <= 0:
					current_room.enemy_list.remove(enemy)
					all_sprites.remove(enemy)

		for m in current_room.enemy_list:
			m.move(current_room.wall_list)

		# drawing (move to screen.py next)

		screen.fill(BLK)
		
		all_sprites.draw(screen)
		try:
			all_sprites.remove(sword)
			sword_list.remove(sword)
		except UnboundLocalError:
			pass
		current_room.wall_list.draw(screen)
		current_room.enemy_list.draw(screen)
		
		pygame.display.flip()
		
		clock.tick(60)
		
	pygame.quit()
	
if __name__ == "__main__":
	main()
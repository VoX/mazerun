import pygame, random, wall
import wall
from constants import *
from gamemap import GameMap
from room import Room
from player import Player
from bullet import Bullet
from sword import Sword
from screen import Screen
from enemy import Enemy
from treasure import Treasure

def main():
	## MAIN GAME LOOP ##
	
	# init pygame
	pygame.init()
	clock = pygame.time.Clock()
	screen = Screen()
	gamemap = GameMap()
	
	# create player paddle
	player = Player(100, 50, 50)
	all_sprites = pygame.sprite.Group()
	moving_sprites = pygame.sprite.Group()
	bullet_list = pygame.sprite.Group()
	sword_list = pygame.sprite.Group()
	weapon_type = 'ranged'

	all_sprites.add(player)
	moving_sprites.add(player)

	# sword swing int
	sword_count = 0
	
	# invulnerability timer
	invuln_count = 0
	
	# create rooms
	# there has to be a better way
	rooms = gamemap.get_rooms()
	
	current_room_num = 0
	current_room = rooms[current_room_num]

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
						bullet = Bullet('up',player.rect.centerx,player.rect.centery-10)
						bullet.fire(0,1)
						all_sprites.add(bullet)
						bullet_list.add(bullet)
					elif event.key == pygame.K_a:
						bullet = Bullet('left',player.rect.centerx-10,player.rect.centery)
						bullet.fire(-1,0)
						all_sprites.add(bullet)
						bullet_list.add(bullet)
					elif event.key == pygame.K_s:
						bullet = Bullet('down',player.rect.centerx,player.rect.centery)
						bullet.fire(0,-1)
						all_sprites.add(bullet)
						bullet_list.add(bullet)
					elif event.key == pygame.K_d:
						bullet = Bullet('right',player.rect.centerx,player.rect.centery)
						bullet.fire(1,0)
						all_sprites.add(bullet)
						bullet_list.add(bullet)
				if weapon_type == 'melee':
					if event.key == pygame.K_w:
						sword = Sword('up',player.rect.centerx,player.rect.centery-10)
						sword.swing(0,1)
						sword_count = 5
						all_sprites.add(sword)
						sword_list.add(sword)
					elif event.key == pygame.K_a:
						sword = Sword('left',player.rect.centerx-12,player.rect.centery)
						sword.swing(-1,0)
						sword_count = 5
						all_sprites.add(sword)
						sword_list.add(sword)
					elif event.key == pygame.K_s:
						sword = Sword('down',player.rect.centerx,player.rect.centery+6)
						sword.swing(0,-1)
						sword_count = 5
						all_sprites.add(sword)
						sword_list.add(sword)
					elif event.key == pygame.K_d:
						sword = Sword('right',player.rect.centerx+6,player.rect.centery)
						sword.swing(1,0)
						sword_count = 5
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
				# deal damage to enemy
				enemy.take_damage(player.ranged_damage, player.rect.x, player.rect.y)
				if enemy.health <= 0:
					current_room.enemy_list.remove(enemy)
					all_sprites.remove(enemy)

			# remove bullet if off screen
				
		for s in sword_list:

			# collision?
			enemy_hit_list = pygame.sprite.spritecollide(s, current_room.enemy_list, False)

			for enemy in enemy_hit_list:
				# deal damage to enemy
				enemy.take_damage(player.melee_damage, player.rect.x, player.rect.y)
				if enemy.health <= 0:
					loot_roll = random.randint(0,30)
					if loot_roll > 15:
						loot = Treasure(enemy.rect.centerx, enemy.rect.centery)
						all_sprites.add(loot)
						current_room.treasure_list.add(loot)
					current_room.enemy_list.remove(enemy)
					all_sprites.remove(enemy)

		for m in current_room.enemy_list:
			m.move(current_room.wall_list)
			enemy_hit_player = pygame.sprite.spritecollide(player, current_room.enemy_list, False)

			for enemy in enemy_hit_player:
				# deal damage to player
				if invuln_count == 0:
					player.take_damage(enemy.damage, enemy.rect.x, enemy.rect.y)
					invuln_count = 1000
					if player.health <= 0:
						pass
				else:
					invuln_count -= 1

		for t in current_room.treasure_list:
			treasure_picked_up = pygame.sprite.spritecollide(player, current_room.treasure_list, True)

			for treasure in treasure_picked_up:
				# pick up loot!
				player.add_loot(treasure)

		# drawing (move to screen.py next)

		if sword_count == 0:
			try:
				all_sprites.remove(sword)
				sword_list.remove(sword)
			except UnboundLocalError:
				pass
			sword_count = 5
		else:
			sword_count -= 1
		screen.screen.fill(BLK)
		
		screen.to_screen(all_sprites)
		screen.to_screen(current_room.wall_list)
		screen.to_screen(current_room.enemy_list)
		screen.draw_stats(player)
		screen.draw_gold(player.gold)
		screen.draw_inventory()
		screen.draw_equipment()
		
		pygame.display.flip()
		
		clock.tick(60)
		
	pygame.quit()
	
if __name__ == "__main__":
	main()
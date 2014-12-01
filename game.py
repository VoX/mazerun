import pygame, random, sys
from constants import *
from gamemap import GameMap
from room import Room
from wall import Wall
from player import Player
from inventory import Inventory
from bullet import Bullet
from sword import Sword
from screen import Screen
from enemy import Enemy
from treasure import Treasure
from expreward import EXPReward

class Game(object):
	## MAIN GAME CLASS
	def __init__(self):
		# init pygame
		self.clock = pygame.time.Clock()
		self.screen = Screen()
		self.gamemap = GameMap()
	
		# create player paddle and inventory
		self.player = Player(100, 50, 50)
		self.inventory = Inventory()

		# create sprite Groups for game logic
		self.all_sprites = pygame.sprite.Group()
		self.moving_sprites = pygame.sprite.Group()
		self.bullet_list = pygame.sprite.Group()
		self.sword_list = pygame.sprite.Group()
		self.reward_list = pygame.sprite.Group()

		# define default weapon type
		self.weapon_type = 'ranged'	

		self.all_sprites.add(self.player)
		self.moving_sprites.add(self.player)	

		# sword swing int
		self.sword_count = 0
	
		# invulnerability timer
		self.invuln_count = 0
		
		# create rooms
		# there has to be a better way
		self.rooms = self.gamemap.get_rooms()
		
		self.current_room_num = 0
		self.current_room = self.rooms[self.current_room_num]

		self.all_sprites.add(self.current_room.enemy_list)
		
		self.run()

	def terminate(self):
		pygame.quit()
		sys.exit()

	def run(self):
	
		while 1:			
			self.clock.tick(60)
			# event processing
		
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.terminate()
			
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.terminate()
					if event.key == pygame.K_LCTRL:
						if self.weapon_type == 'ranged':
							self.weapon_type = 'melee'
						else:
							self.weapon_type = 'ranged'
					if event.key == pygame.K_LEFT:
						self.player.change_speed(-5, 0)
					if event.key == pygame.K_RIGHT:
						self.player.change_speed(5, 0)
					if event.key == pygame.K_UP:
						self.player.change_speed(0, -5)
					if event.key == pygame.K_DOWN:
						self.player.change_speed(0, 5)
					if self.weapon_type == 'ranged':
						if event.key == pygame.K_w:
							bullet = Bullet('up',self.player.rect.centerx,
								self.player.rect.centery-10)
							bullet.fire(0,1)
							self.all_sprites.add(bullet)
							self.bullet_list.add(bullet)
						elif event.key == pygame.K_a:
							bullet = Bullet('left',self.player.rect.centerx-10,
								self.player.rect.centery)
							bullet.fire(-1,0)
							self.all_sprites.add(bullet)
							self.bullet_list.add(bullet)
						elif event.key == pygame.K_s:
							bullet = Bullet('down',self.player.rect.centerx,
								self.player.rect.centery)
							bullet.fire(0,-1)
							self.all_sprites.add(bullet)
							self.bullet_list.add(bullet)
						elif event.key == pygame.K_d:
							bullet = Bullet('right',self.player.rect.centerx,
								self.player.rect.centery)
							bullet.fire(1,0)
							self.all_sprites.add(bullet)
							self.bullet_list.add(bullet)
					if self.weapon_type == 'melee':
						if event.key == pygame.K_w:
							sword = Sword('up',self.player.rect.centerx,
								self.player.rect.centery-10)
							sword.swing(0,1)
							self.sword_count = 5
							self.all_sprites.add(sword)
							self.sword_list.add(sword)
						elif event.key == pygame.K_a:
							sword = Sword('left',self.player.rect.centerx-12,
								self.player.rect.centery)
							sword.swing(-1,0)
							self.sword_count = 5
							self.all_sprites.add(sword)
							self.sword_list.add(sword)
						elif event.key == pygame.K_s:
							sword = Sword('down',self.player.rect.centerx,
								self.player.rect.centery+6)
							sword.swing(0,-1)
							self.sword_count = 5
							self.all_sprites.add(sword)
							self.sword_list.add(sword)
						elif event.key == pygame.K_d:
							sword = Sword('right',self.player.rect.centerx+6,
								self.player.rect.centery)
							sword.swing(1,0)
							self.sword_count = 5
							self.all_sprites.add(sword)
							self.sword_list.add(sword)
						
			
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_LEFT:
						self.player.change_speed(5, 0)
					if event.key == pygame.K_RIGHT:
						self.player.change_speed(-5, 0)
					if event.key == pygame.K_UP:
						self.player.change_speed(0, 5)
					if event.key == pygame.K_DOWN:
						self.player.change_speed(0, -5)
					
			# game logic
		
			self.player.move(self.current_room.wall_list)
		
			if self.player.rect.x < -15:
				# cleanup bullets on room-change
				# there must be a better way to do this
				for b in self.bullet_list:
					self.bullet_list.remove(b)
					self.all_sprites.remove(b)
				# room change logic
				if self.current_room_num == 0:
					self.current_room_num = 2
					self.current_room = self.rooms[self.current_room_num]
					self.player.rect.x = 790
					
				elif self.current_room_num == 2:
					self.player.rect.x = 790
					self.current_room_num = 1
					self.current_room = self.rooms[self.current_room_num]
				
				else:
					self.current_room_num = 0
					self.current_room = self.rooms[self.current_room_num]
					self.player.rect.x = 790
				
			if self.player.rect.x > 801:
				# cleanup bullets on room-change
				# there must be a better way to do this
				for b in self.bullet_list:
					self.bullet_list.remove(b)
					self.all_sprites.remove(b)
				if self.current_room_num == 0:
					self.current_room_num = 1
					self.current_room = self.rooms[self.current_room_num]
					self.player.rect.x = 0
				elif self.current_room_num == 1:
					self.current_room_num = 2
					self.current_room = self.rooms[self.current_room_num]
					self.player.rect.x = 0
				else:
					self.current_room_num = 0
					self.current_room = self.rooms[self.current_room_num]
					self.player.rect.x = 0

			for b in self.bullet_list:

				# collision?
				b.move()
				block_hit_list = pygame.sprite.spritecollide(b,
							self.current_room.wall_list, False)
				enemy_hit_list = pygame.sprite.spritecollide(b,
							self.current_room.enemy_list, False)

				# remove bullet
				for block in block_hit_list:
					self.bullet_list.remove(b)
					self.all_sprites.remove(b)

				for enemy in enemy_hit_list:
					self.bullet_list.remove(b)
					self.all_sprites.remove(b)
					# deal damage to enemy
					enemy.take_damage(self.player.ranged_damage,
							self.player.rect.x, self.player.rect.y)
					if enemy.health <= 0:
						self.current_room.enemy_list.remove(enemy)
						self.all_sprites.remove(enemy)

						self.player.earn_EXP(enemy.EXP)

						loot_roll = random.randint(0,30)
						if loot_roll > 15:
							loot = Treasure(enemy.rect.centerx, enemy.rect.centery)
							self.all_sprites.add(loot)
							self.current_room.treasure_list.add(loot)
						self.reward_list.add(EXPReward(enemy.rect.centerx,
							enemy.rect.centery-TILE_SIZE, enemy.EXP))

			# remove bullet if off screen
				
			for s in self.sword_list:

				# collision?
				enemy_hit_list = pygame.sprite.spritecollide(s,
							self.current_room.enemy_list, False)

				for enemy in enemy_hit_list:
					# deal damage to enemy
					if self.sword_count == 5:
						enemy.take_damage(self.player.melee_damage,
									self.player.rect.x, self.player.rect.y)
					if enemy.health <= 0:
						self.current_room.enemy_list.remove(enemy)
						self.all_sprites.remove(enemy)

						self.player.earn_EXP(enemy.EXP)

						loot_roll = random.randint(0,30)
						if loot_roll > 15:
							loot = Treasure(enemy.rect.centerx, enemy.rect.centery)
							self.all_sprites.add(loot)
							self.current_room.treasure_list.add(loot)
						self.reward_list.add(EXPReward(enemy.rect.centerx,
							enemy.rect.centery-TILE_SIZE, enemy.EXP))
						

			for m in self.current_room.enemy_list:
				m.move(self.current_room.wall_list)
				enemy_hit_player = pygame.sprite.spritecollide(self.player,
										self.current_room.enemy_list, False)

				for enemy in enemy_hit_player:
					# deal damage to player
					if self.invuln_count == 0:
						self.player.take_damage(enemy.damage, enemy.rect.x, enemy.rect.y)
						self.invuln_count = 1000
						if self.player.health <= 0:
							pass
					else:
						self.invuln_count -= 1

			for t in self.current_room.treasure_list:
				treasure_picked_up = pygame.sprite.spritecollide(self.player,
								self.current_room.treasure_list, True)

				for treasure in treasure_picked_up:
					# pick up loot!
					self.add_treasure(treasure)
					self.screen.draw_inventory(self.inventory)
					self.screen.draw_equipment(self.player.equipped)

			for r in self.reward_list:
				r.counter -= 1
				if r.counter == 0:
					self.reward_list.remove(r)

			if self.sword_count == 0:
				try:
					self.all_sprites.remove(sword)
					self.sword_list.remove(sword)
				except UnboundLocalError:
					pass
			else:
				self.sword_count -= 1
			self.screen.screen.fill(BLK)
			
			self.screen.to_screen(self.all_sprites)
			self.screen.to_screen(self.current_room.wall_list)
			self.screen.to_screen(self.current_room.enemy_list)
			self.screen.to_screen(self.reward_list)
			self.screen.draw_stats(self.player)
			self.screen.draw_gold(self.player.gold)
			self.screen.draw_inventory(self.inventory)
			self.screen.draw_equipment(self.player.equipped)
			
			pygame.display.flip()
			
		pygame.quit()

	def add_treasure(self, treasure):
		text = 'You found %s. %s' % (treasure.title, treasure.desc)
		self.inventory.add_to_inventory(treasure, self.player)
		self.screen.draw_alert(text)
	
if __name__ == "__main__":
	main()
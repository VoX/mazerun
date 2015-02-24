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
		self.player_list = pygame.sprite.Group()
		self.bullet_list = pygame.sprite.Group()
		self.sword_list = pygame.sprite.Group()
		self.expReward_list = pygame.sprite.Group()

		# define default weapon type
		self.weapon_type = 'ranged'	

		self.player_list.add(self.player)	

		# sword swing int
		self.sword_count = 0
	
		# invulnerability timer
		self.invuln_count = 0
		
		# create rooms
		# there has to be a better way
		self.rooms = self.gamemap.get_rooms()
		
		self.current_room_num = 0
		self.current_room = self.rooms[self.current_room_num]
		
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
					self.keyboardDown(event)
						
				if event.type == pygame.KEYUP:
					self.keyboardUp(event)
					
			# game logic
		
			self.modelUpdate()
			self.viewerUpdate(self.screen)
			
		pygame.quit()

	def add_treasure(self, treasure):
		text = 'You found %s. %s' % (treasure.title, treasure.desc)
		self.inventory.add_to_inventory(treasure, self.player)
		self.screen.draw_alert(text)

	def blit_alpha(self, target, source, location, opacity):
		x = location[0]
		y = location[1]
		temp = pygame.Surface((source.get_width(), source.get_height())).convert()
		temp.blit(target, (-x, -y))
		temp.blit(source, (0, 0))
		temp.set_alpha(opacity)        
		target.blit(temp, location)
		
	def keyboardDown(self, evt):
		if evt.key == pygame.K_ESCAPE:
			self.terminate()
		if evt.key == pygame.K_LCTRL:
			self.weaponSelect()
		if evt.key == pygame.K_LEFT:
			self.player.change_speed(-5, 0)
		if evt.key == pygame.K_RIGHT:
			self.player.change_speed(5, 0)
		if evt.key == pygame.K_UP:
			self.player.change_speed(0, -5)
		if evt.key == pygame.K_DOWN:
			self.player.change_speed(0, 5)
			
		if self.weapon_type == 'ranged':
			self.shootBullet(evt)
				
		if self.weapon_type == 'melee':
			self.swingSword(evt)
					
	def keyboardUp(self, evt):
		if evt.key == pygame.K_LEFT:
			self.player.change_speed(5, 0)
		if evt.key == pygame.K_RIGHT:
			self.player.change_speed(-5, 0)
		if evt.key == pygame.K_UP:
			self.player.change_speed(0, 5)
		if evt.key == pygame.K_DOWN:
			self.player.change_speed(0, -5)
			
	def modelUpdate(self):
		self.player.move(self.current_room.wall_list)

		for b in self.bullet_list:
			self.bulletLogic(b)
				
		for s in self.sword_list:
			self.swordLogic(s)
			
		for m in self.current_room.enemy_list:
			self.monsterLogic(m)

		for l in self.current_room.treasure_list:
			self.lootLogic(l)

		for r in self.expReward_list:
			r.counter -= 1
			if r.counter == 0:
				self.expReward_list.remove(r)

		if self.sword_count == 0:
			try:
				self.sword_list.remove(s)
			except UnboundLocalError:
				pass
		else:
			self.sword_count -= 1
			
	def shootBullet(self, evt):
		if evt.key == pygame.K_w:
			bullet = Bullet('up',self.player.rect.centerx,
						self.player.rect.centery-10)
			bullet.fire(0,1)
			self.bullet_list.add(bullet)
		elif evt.key == pygame.K_a:
			bullet = Bullet('left',self.player.rect.centerx-10,
						self.player.rect.centery)
			bullet.fire(-1,0)
			self.bullet_list.add(bullet)
		elif evt.key == pygame.K_s:
			bullet = Bullet('down',self.player.rect.centerx,
						self.player.rect.centery)
			bullet.fire(0,-1)
			self.bullet_list.add(bullet)
		elif evt.key == pygame.K_d:
			bullet = Bullet('right',self.player.rect.centerx,
						self.player.rect.centery)
			bullet.fire(1,0)
			self.bullet_list.add(bullet)
	
	def swingSword(self, evt):
		if evt.key == pygame.K_w:
			sword = Sword('up',self.player.rect.centerx,
						self.player.rect.centery-10)
			sword.swing(0,1)
			self.sword_count = 5
			self.sword_list.add(sword)
		elif evt.key == pygame.K_a:
			sword = Sword('left',self.player.rect.centerx-12,
						self.player.rect.centery)
			sword.swing(-1,0)
			self.sword_count = 5
			self.sword_list.add(sword)
		elif evt.key == pygame.K_s:
			sword = Sword('down',self.player.rect.centerx,
						self.player.rect.centery+6)
			sword.swing(0,-1)
			self.sword_count = 5
			self.sword_list.add(sword)
		elif evt.key == pygame.K_d:
			sword = Sword('right',self.player.rect.centerx+6,
						self.player.rect.centery)
			sword.swing(1,0)
			self.sword_count = 5
			self.sword_list.add(sword)
	
	def viewerUpdate(self, screen):
		# updates visual elements
		screen.screen.fill(BLK)
		screen.mapSurf.fill(screen.bgcolor);
		screen.spriteSurf.fill(screen.bgcolor);
		screen.GUISurf.fill(screen.bgcolor);
		
		screen.to_screen(self.current_room.wall_list, screen.mapSurf)
		screen.to_screen(self.current_room.enemy_list, screen.spriteSurf)
		screen.to_screen(self.current_room.treasure_list, screen.spriteSurf)
		screen.to_screen(self.expReward_list, screen.spriteSurf)
		screen.to_screen(self.bullet_list, screen.spriteSurf)
		screen.to_screen(self.sword_list, screen.spriteSurf)
		screen.to_screen(self.player_list, screen.spriteSurf)
		screen.draw_stats(self.player)
		screen.draw_gold(self.player.gold)
		screen.draw_inventory(self.inventory)
		screen.draw_equipment(self.player.equipped)
		
		screen.update()
			
		pygame.display.flip()
	
	def weaponSelect(self):
		# allows swapping between weapons
		if self.weapon_type == 'ranged':
			self.weapon_type = 'melee'
		else:
			self.weapon_type = 'ranged'
	
	def bulletLogic(self, b):

		# collision?
		b.move()
		block_hit_list = pygame.sprite.spritecollide(b,
					self.current_room.wall_list, False)
		enemy_hit_list = pygame.sprite.spritecollide(b,
					self.current_room.enemy_list, False)
		# remove bullet
		for block in block_hit_list:
			self.bullet_list.remove(b)

		for enemy in enemy_hit_list:
			self.bullet_list.remove(b)
			# deal damage to enemy
			self.damageLogic(enemy, self.player,
					self.player.ranged_damage())
			
	def damageLogic(self, target, attacker, damage):
		# handles damage dealing
		target.take_damage(damage, attacker.rect.x,
				attacker.rect.y)
		if target.health <= 0:
			# if dead, removes from visual list
			self.current_room.enemy_list.remove(target)
			
			# rewards EXP to attacker
			# this function will need to be adjusted
			# to allow player-kill EXP rewards
			attacker.earn_EXP(target.EXP)

			loot_roll = random.randint(0,30)
			# roll for loot
			if loot_roll > 15:
				loot = Treasure(target.rect.centerx, target.rect.centery)
				self.current_room.treasure_list.add(loot)
			# create EXP reward visual
			self.expReward_list.add(EXPReward(target.rect.centerx,
				target.rect.centery-TILE_SIZE, target.EXP))

	def swordLogic(self, s):

		# collision?
		enemy_hit_list = pygame.sprite.spritecollide(s,
					self.current_room.enemy_list, False)

		for enemy in enemy_hit_list:
			# deal damage to enemy
			if self.sword_count == 5:
				self.damageLogic(enemy, self.player,
						self.player.melee_damage())

	def monsterLogic(self, m):
	
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
	
	def lootLogic(self, l):
		treasure_picked_up = pygame.sprite.spritecollide(self.player,
						self.current_room.treasure_list, True)

		for treasure in treasure_picked_up:
			# pick up loot!
			self.add_treasure(treasure)
			self.screen.draw_inventory(self.inventory)
			self.screen.draw_equipment(self.player.equipped)
	
if __name__ == "__main__":
	main()
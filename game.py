import pygame
from pygame.locals import *
from constants import *
from player import Player
from bullet import Bullet
from sword import Sword
from enemy import Enemy



class Game(object):

	def __init__(self):	
		self.weapon_type = 'ranged'
		
	def event_process(self, player):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					done = True
				if event.key == pygame.K_LCTRL:
					if self.weapon_type == 'ranged':
						self.weapon_type = 'melee'
					else:
						self.weapon_type = 'ranged'
				if event.key == pygame.K_LEFT:
					player.change_speed(-5, 0)
				if event.key == pygame.K_RIGHT:
					player.change_speed(5, 0)
				if event.key == pygame.K_UP:
					player.change_speed(0, -5)
				if event.key == pygame.K_DOWN:
					player.change_speed(0, 5)
				if self.weapon_type == 'ranged':
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
				if self.weapon_type == 'melee':
					if event.key == pygame.K_w:
						sword = Sword('up',player.rect.centerx,player.rect.centery-10)
						sword.swing(0,1)
						count = 1
						all_sprites.add(sword)
						sword_list.add(sword)
					elif event.key == pygame.K_a:
						sword = Sword('left',player.rect.centerx-12,player.rect.centery)
						sword.swing(-1,0)
						count = 1
						all_sprites.add(sword)
						sword_list.add(sword)
					elif event.key == pygame.K_s:
						sword = Sword('down',player.rect.centerx,player.rect.centery+6)
						sword.swing(0,-1)
						count = 1
						all_sprites.add(sword)
						sword_list.add(sword)
					elif event.key == pygame.K_d:
						sword = Sword('right',player.rect.centerx+6,player.rect.centery)
						sword.swing(1,0)
						count = 1
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
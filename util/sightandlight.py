''' 
    SIGHT & LIGHT by ncase (https://github.com/ncase/sight-and-light)
    Ported to Python/PyGame by Marcus Moller (https://github.com/marcusmoller)
'''

import pygame
import pygame.gfxdraw
import math

class SightAndLight():
	def __init__(self, player_pos, wall_list):
		self.player_pos = player_pos
		self.wall_list = wall_list

		self.segments = []

		for block in self.wall_list:
			segment = [
				{'a':{'x': block.rect.topleft[0],'y': block.rect.bottomleft[1]},
				'b':{'x': block.rect.topright[0],'y': block.rect.topright[1]}},

				{'a':{'x': block.rect.topright[0],'y': block.rect.topright[1]},
				'b':{'x': block.rect.bottomright[0],'y': block.rect.bottomright[1]}},

				{'a':{'x': block.rect.bottomright[0],'y': block.rect.bottomright[1]},
				'b':{'x': block.rect.bottomleft[0],'y': block.rect.bottomleft[1]}},

				{'a':{'x': block.rect.bottomleft[0],'y': block.rect.bottomleft[1]},
				'b':{'x': block.rect.bottomleft[0],'y': block.rect.bottomleft[1]}}
			]
			self.segments.append(segment)

		self.intersects = []

		self.points = []

	def update(self):
		# clear old points
		self.points = []

		# get unique points
		for segment_group in self.segments:
			for segment in segment_group:
				self.points.append((segment['a'], segment['b']))

		unique_points = []
		for point in self.points:
			if point not in unique_points:
				unique_points.append(point)

		# get all angles
		unique_angles = []
		for point in unique_points:
			angle = math.atan2(point[0]['y']-self.player_pos[1],
				point[0]['x']-self.player_pos[0])
			point[0]['angle'] = angle
			unique_angles.append(angle-0.00001)
			unique_angles.append(angle)
			unique_angles.append(angle+0.00001)

		# RAYS IN ALL DIRECTIONS
		self.intersects = []
		for angle in unique_angles:
			# calculate dx/dy
			dx = math.cos(angle)
			dy = math.sin(angle)

			# ray from center to player
			ray = {
				'a': {'x':self.player_pos[0], 'y':self.player_pos[1]},
				'b': {'x':self.player_pos[0]+dx, 'y':self.player_pos[1]+dy}
			}

			# find closest intersection
			closest_intersect = None
			for segment_group in self.segments:
				for segment in segment_group:
					intersect = self.get_intersection(ray, segment)
					if not intersect: continue
					if not closest_intersect or intersect['param'] < closest_intersect['param']:
						closest_intersect = intersect

			# intersect angle
			if not closest_intersect: continue
			closest_intersect['angle'] = angle

			# add to list of intersects
			self.intersects.append(closest_intersect)

		# sort intersects by angle
		self.intersects = sorted(self.intersects, key=lambda k: k['angle'])

	def render_frame(self, screen):
		self.screen = screen
		self.screen.fill((255,255,255))

		# draw segments
		for segment in self.segments:
			pygame.draw.aaline(self.screen, (153, 153, 153),
				(segment['a']['x'], segment['a']['y']),
				segment['b']['x'], segment['b']['y'])

		self.draw_polygon(self.intersects, (221, 56, 56))

		# draw debug lines
		for intersect in self.intersects:
			pygame.draw.aaline(self.screen, (255, 85, 85), self.player_pos,
				(intersect['x'], intersect['y']))

	def get_intersection(self, ray, segment):
		# RAY in parametric: point + direction*T1
		r_px = ray['a']['x']
		r_py = ray['a']['y']
		r_dx = ray['b']['x'] - ray['a']['x']
		r_dy = ray['b']['y'] - ray['a']['y']

		# SEGMENT in parametric: point + direction*T2
		s_px = segment['a']['x']
		s_py = segment['a']['y']
		s_dx = segment['b']['x'] - segment['a']['x']
		s_dy = segment['b']['y'] - segment['a']['y']

		# are they parallel? if so no intersect
		r_mag = math.sqrt(r_dx*r_dx+r_dy*r_dy)
		s_mag = math.sqrt(s_dx*s_dx+s_dy*s_dy)
		try:
			r_dx/r_mag
		except ZeroDivisionError:
			r_mag += 0.01

		try:
			s_dx/s_mag
		except ZeroDivisionError:
			s_mag += 0.01

		try:
			r_dy/r_mag
		except ZeroDivisionError:
			r_mag == 0.01

		try:
			s_dy/s_mag
		except ZeroDivisionError:
			s_mag += 0.01


		if r_dx/r_mag == s_dx/s_mag and r_dy/r_mag == s_dy/s_mag:
			return None

		try:
			T2 = (r_dx*(s_py-r_py) + r_dy*(r_px-s_px))/(s_dx*r_dy - s_dy*r_dx)
		except ZeroDivisionError:
			T2 = (r_dx*(s_py-r_py) + r_dy*(r_px-s_px))/(s_dx*r_dy - s_dy*r_dx-0.01)

		try:
			T1 = (s_px+s_dx*T2-r_px)/r_dx
		except ZeroDivisionError:
			T1 = (s_px+s_dx*T2-r_px)/(r_dx-0.01)

		# must be within parametric whatevers for RAY/SEGMENT
		if T1 < 0: return None
		if T2 < 0 or T2 > 1: return None

		# return POINT OF INTERSECTION
		return {
			'x': r_px+r_dx*T1,
			'y': r_py+r_dy*T1,
			'param': T1
		}

	def draw_polygon(self, polygon, color):
		# collect coordinates for giant polygon
		points = []
		for intersect in polygon:
			points.append((intersect['x'], intersect['y']))

		# draw as giant polygon
		pygame.gfxdraw.aapolygon(self.screen, points, color)
		pygame.gfxdraw.filled_polygon(self.screen, points, color)

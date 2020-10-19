from hw2.entities.base import Agent
from hw2.common import *
import pygame
import math
from random import uniform
from typing import List


class Boid(Agent):

	def __init__(self, screen, x, y, name, radius, direction):
		super().__init__(screen, x, y, name, radius)
		self.direction = direction
		self.speed = 1
		self.nr_ticks = 0

	def check_collision(self, observation: List[Agent]):
		for agent in observation:
			new_x = self.x + self.speed * math.cos(self.direction)
			new_y = self.y + self.speed * math.sin(self.direction)
			if agent.x != self.x or agent.y != self.y:
				if abs(agent.x - new_x) <= self.radius * 2 and abs(agent.y - new_y) <= self.radius * 2:
					if agent.x == SCREEN_SIZE - agent.radius or agent.x == agent.radius:
						self.direction = (MAX_RADIANS - self.direction) - MAX_RADIANS / 2
					else:
						self.direction = MAX_RADIANS - self.direction
					self.nr_ticks = 0

	def draw(self):
		self.update_position()
		pygame.draw.polygon(self.screen, GREEN, self.draw_triangle())

	def draw_triangle(self):
		x = self.x
		y = self.y

		p1 = (x + 3 * self.radius, y)
		p2 = (x, y - self.radius)
		p3 = (x, y + self.radius)

		_cos = math.cos(self.direction)
		_sin = math.sin(self.direction)

		p1 = (_cos * (p1[0] - x) - _sin * (p1[1] - y) + x), (_sin * (p1[0] - x) + _cos * (p1[1] - y) + y)
		p2 = (_cos * (p2[0] - x) - _sin * (p2[1] - y) + x), (_sin * (p2[0] - x) + _cos * (p2[1] - y) + y)
		p3 = (_cos * (p3[0] - x) - _sin * (p3[1] - y) + x), (_sin * (p3[0] - x) + _cos * (p3[1] - y) + y)

		return [p1, p2, p3]

	def update_direction(self):
		down_value = max(self.direction - CORRECTION_RADIANS, 0)
		up_value = min(self.direction + CORRECTION_RADIANS, MAX_RADIANS)
		self.direction = uniform(down_value, up_value)

	def update_position(self):
		self.x += self.speed * math.cos(self.direction)
		self.y += self.speed * math.sin(self.direction)
		self.nr_ticks += 1

		# if self.nr_ticks == 10:
		# 	self.update_direction()
		# 	self.nr_ticks = 0

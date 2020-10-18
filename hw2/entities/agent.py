from hw2.entities.base import Agent
from hw2.common import *
import pygame
import math
from random import uniform


class Boid(Agent):

	def __init__(self, screen, x, y, name, radius, direction):
		super().__init__(screen, x, y, name, radius)
		self.direction = direction
		self.orientation = (direction + CORRECTION_RADIANS) % MAX_RADIANS
		self.speed = 1

		self.nr_ticks = 0

	def draw(self):
		self.update_position()
		pygame.draw.polygon(self.screen, GREEN, self.draw_triangle())

	def draw_triangle(self):
		x = self.x
		y = self.y

		p1 = (x, y - 3 * self.radius)
		p2 = (x - self.radius, y)
		p3 = (x + self.radius, y)

		_cos = math.cos(self.orientation)
		_sin = math.sin(self.orientation)

		p1 = (_cos * (p1[0] - x) - _sin * (p1[1] - y) + x), (_sin * (p1[0] - x) + _cos * (p1[1] - y) + y)
		p2 = (_cos * (p2[0] - x) - _sin * (p2[1] - y) + x), (_sin * (p2[0] - x) + _cos * (p2[1] - y) + y)
		p3 = (_cos * (p3[0] - x) - _sin * (p3[1] - y) + x), (_sin * (p3[0] - x) + _cos * (p3[1] - y) + y)

		return [p1, p2, p3]

	def update_direction(self):
		down_value = max(self.direction- CORRECTION_RADIANS, 0)
		up_value = min(self.direction + CORRECTION_RADIANS, MAX_RADIANS)
		self.direction = uniform(down_value, up_value)
		self.orientation = (self.direction + CORRECTION_RADIANS) % MAX_RADIANS

	def update_position(self):
		self.x += self.speed * math.cos(self.direction)
		self.y += self.speed * math.sin(self.direction)
		self.nr_ticks += 1

		if self.nr_ticks == 20:
			self.update_direction()
			self.nr_ticks = 0


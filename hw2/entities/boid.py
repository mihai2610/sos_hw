from hw2.entities.base import Agent
from hw2.common import *
import pygame
import math
from random import uniform
from typing import List
import numpy as np

vec = pygame.math.Vector2


class Boid(Agent):

	def __init__(self, screen, x, y, name, radius):
		super().__init__(screen, x, y, name, radius)
		self.position = vec(x, y)
		self.velocity = vec(uniform(-1, 1), uniform(-1, 1))
		self.acceleration = 0.3
		self.max_speed = 5
		self.perception = 50

	def check_collision(self, observation: List[Agent]):
		for agent in observation:
			if agent != self:
				nv = self.position - agent.position
				dist = np.linalg.norm(nv)
				if dist < 2 * self.radius:
					nv = pygame.math.Vector2(nv) / dist
					self.velocity = pygame.math.Vector2(self.velocity).reflect(nv)

	def align(self, agents: List[Agent]):
		avg_vec = vec(0, 0)
		count = 0

		for agent in agents:
			if agent.name == BOID_NAME and agent != self:
				if np.linalg.norm(agent.position - self.position) < self.perception:
					avg_vec += agent.velocity
					count += 1

		if count > 0:
			avg_vec /= count
			avg_vec /= np.linalg.norm(avg_vec)

		return avg_vec

	def cohesion(self, agents: List[Agent]):
		count = 0
		avg_position = vec(0, 0)

		for agent in agents:
			if agent.name == BOID_NAME and agent != self:
				if np.linalg.norm(agent.position - self.position) < self.perception:
					avg_position += agent.position
					count += 1

		if count > 0:
			avg_position /= count
			avg_position -= self.position
			avg_position /= np.linalg.norm(avg_position)

		return avg_position

	def separation(self, agents: List[Agent]):
		avg_vector = vec(0, 0)

		for agent in agents:
			if agent != self:
				distance = np.linalg.norm(agent.position - self.position)

				if distance < self.perception:
					avg_vector += (self.position - agent.position) / distance

		return avg_vector

	def draw(self):
		pygame.draw.polygon(self.screen, GREEN, self.draw_triangle())

	def draw_triangle(self):
		x = self.position[0]
		y = self.position[1]

		p1 = (x + 3 * self.radius, y)
		p2 = (x, y - self.radius)
		p3 = (x, y + self.radius)

		angle = math.atan2(self.velocity[1], self.velocity[0])
		_cos = math.cos(angle)
		_sin = math.sin(angle)

		p1 = (_cos * (p1[0] - x) - _sin * (p1[1] - y) + x), (_sin * (p1[0] - x) + _cos * (p1[1] - y) + y)
		p2 = (_cos * (p2[0] - x) - _sin * (p2[1] - y) + x), (_sin * (p2[0] - x) + _cos * (p2[1] - y) + y)
		p3 = (_cos * (p3[0] - x) - _sin * (p3[1] - y) + x), (_sin * (p3[0] - x) + _cos * (p3[1] - y) + y)

		return [p1, p2, p3]

	def update_position(self, agents: List[Agent]):

		self.velocity += self.separation(agents)
		self.velocity += self.cohesion(agents)
		self.velocity += self.align(agents)

		self.check_collision(agents)

		self.position += self.velocity
		self.velocity += self.velocity * (self.acceleration / np.linalg.norm(self.velocity))

		if np.linalg.norm(self.velocity) > self.max_speed:
			self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed

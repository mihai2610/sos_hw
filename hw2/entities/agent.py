from hw2.entities.base import Agent
from hw2.common import *
import pygame
import math
from random import uniform
from typing import List
import numpy as np

vec = pygame.math.Vector2


class Boid(Agent):

	def __init__(self, screen, x, y, name, radius, direction):
		super().__init__(screen, x, y, name, radius)
		self.direction = direction
		self.speed = 1
		self.nr_ticks = 0
		self.position = vec(x, y)
		self.velocity = vec(uniform(-1, 1), uniform(-1, 1))
		self.acceleration = vec(0.1, 0.1)
		self.angle = 0
		self.max_force = 0.3
		self.max_speed = 7
		self.perception = 70

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
			if agent.name == BOID_NAME:
				if np.linalg.norm(agent.position - self.position) < self.perception:
					avg_vec += agent.velocity
					count += 1

		if count > 0:
			avg_vec = (avg_vec / np.linalg.norm(avg_vec)) * self.max_speed
			avg_vec -= self.velocity

		return avg_vec

	def cohesion(self, agents: List[Agent]):
		steering = vec(0, 0)
		count = 0
		avg_position = vec(0, 0)

		for agent in agents:
			if agent.name == BOID_NAME:
				if np.linalg.norm(agent.position - self.position) < self.perception:
					avg_position += agent.position
					count += 1

		if count > 0:
			temp_vec = avg_position / count - self.position
			if np.linalg.norm(temp_vec) > 0:
				temp_vec = (temp_vec / np.linalg.norm(temp_vec)) * self.max_speed

			steering = temp_vec - self.velocity

			if np.linalg.norm(steering) > self.max_force:
				steering = (steering / np.linalg.norm(steering)) * self.max_force

		return steering

	def separation(self, agents: List[Agent]):
		steering = vec(*np.zeros(2))
		count = 0
		avg_vector = vec(*np.zeros(2))
		for agent in agents:
			if agent.name == BOID_NAME:
				distance = np.linalg.norm(agent.position - self.position)
				if self.position != agent.position and distance < self.perception:
					avg_vector += (self.position - agent.position) / distance
					count += 1
		if count > 0:
			avg_vector /= count
			if np.linalg.norm(steering) > 0:
				avg_vector = (avg_vector / np.linalg.norm(steering)) * self.max_speed
			steering = avg_vector - self.velocity
			if np.linalg.norm(steering) > self.max_force:
				steering = (steering / np.linalg.norm(steering)) * self.max_force

		return steering

	def apply_rules(self, agents: List[Agent]):
		self.acceleration += self.align(agents)
		self.acceleration += self.cohesion(agents)
		self.acceleration += self.separation(agents)

	def draw(self):
		self.update_position()
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

	def update_position(self):
		self.position += self.velocity
		self.velocity += self.acceleration
		# limit

		if np.linalg.norm(self.velocity) > self.max_speed:
			self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed

		self.acceleration = vec(0, 0)

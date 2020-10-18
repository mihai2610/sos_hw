from hw2.entities.agent import Boid
from hw2.entities.obstacle import Obstacle
from hw2.entities.base import Agent
from hw2.common import *

from typing import List
from random import uniform


class Environment:

	def __init__(self, radius, screen):
		self.agents: List[Agent] = []
		self.radius = radius
		self.screen = screen

	def add_boid(self, mouse_x, mouse_y):
		direction = uniform(0, MAX_RADIANS)
		boid = Boid(self.screen, mouse_x, mouse_y, BOID_NAME, self.radius, direction)
		self.agents.append(boid)

	def add_obstacle(self, mouse_x, mouse_y):
		obstacle = Obstacle(self.screen, mouse_x, mouse_y, OBSTACLE_NAME, self.radius)
		self.agents.append(obstacle)

from hw2.entities.agent import Boid
from hw2.entities.obstacle import Obstacle
from hw2.entities.base import Agent
from hw2.common import *

from typing import List


class Environment:

	def __init__(self, radius, screen):
		self.agents: List[Agent] = []
		self.radius = radius
		self.screen = screen
		self.boid_nr = 0
		self.obstacle_nr = 0

	def add_boid(self, mouse_x, mouse_y):
		radius = 3
		boid = Boid(self.screen, mouse_x, mouse_y, BOID_NAME, radius)
		self.agents.append(boid)
		self.boid_nr += 1

	def add_obstacle(self, mouse_x, mouse_y):
		obstacle = Obstacle(self.screen, mouse_x, mouse_y, OBSTACLE_NAME, self.radius)
		self.agents.append(obstacle)
		self.obstacle_nr += 1

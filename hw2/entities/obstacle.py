from hw2.entities.base import Agent
from hw2.common import RED
import pygame


class Obstacle(Agent):

	def __init__(self, screen, x, y, name, radius=0):
		super().__init__(screen, x, y, name, radius)

	def draw(self):
		pygame.draw.circle(self.screen, RED, (self.x, self.y), self.radius)

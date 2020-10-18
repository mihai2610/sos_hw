import pygame
import sys
from math import pi, cos, sin, sqrt
from typing import List
import math

current = None
lag = 0.0
ticks, fps = 0, 0

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


# configuration = config.GameConfiguration()

class Agent(object):

	def __init__(self, screen, x: float, y: float, name: str, radius: float = 2):
		self.x = x
		self.y = y
		self.radius = radius
		self.name = name
		self.screen = screen

	def __str__(self):
		return "Agent {} : ({}, {})".format(self.name, self.x, self.y)

	def draw(self):
		raise NotImplementedError


class Boid(Agent):

	def __init__(self, screen, x, y, name, radius, direction):
		super().__init__(screen, x, y, name, radius)
		self.direction = direction
		self.speed = 1

	def draw(self):
		self.update_position()
		pygame.draw.polygon(self.screen, GREEN, self.draw_triangle())

	def draw_triangle(self):
		x = self.x
		y = self.y

		p1 = (x, y - 2 * self.radius)
		p2 = (x - self.radius, y)
		p3 = (x + self.radius, y)

		# if self.direction != 0:
		# angle = math.atan2(self.x - curx, self.y - cury)

		_cos = math.cos(self.direction)
		_sin = math.sin(self.direction)

		# p1 = (_cos * p1[0] - p1[0] + _sin * p1[1]), (_sin * p1[0] + _cos * p1[1] - p1[1])
		# p2 = (_cos * p2[0] - p2[0] - _sin * p2[1]), (_sin * p2[0] + _cos * p2[1] - p2[1])
		# p3 = (_cos * p3[0] - p3[0] - _sin * p3[1]), (_sin * p3[0] + _cos * p3[1] - p3[1])

		p1 = (_cos * (p1[0] - x) - _sin * (p1[1] - y) + x), (_sin * (p1[0] - x) + _cos * (p1[1] - y) + y)
		p2 = (_cos * (p2[0] - x) - _sin * (p2[1] - y) + x), (_sin * (p2[0] - x) + _cos * (p2[1] - y) + y)
		p3 = (_cos * (p3[0] - x) - _sin * (p3[1] - y) + x), (_sin * (p3[0] - x) + _cos * (p3[1] - y) + y)

		return [p1, p2, p3]

	def update_direction(self, dir_x, dir_y):
		self.direction = math.atan2(self.x - dir_x, self.y - dir_y)

	def update_position(self):
		self.x += self.speed * math.cos(math.radians(self.direction))
		self.y += self.speed * math.sin(math.radians(self.direction))


class Obstacle(Agent):

	def __init__(self, screen, x, y, name, radius=0):
		super().__init__(screen, x, y, name, radius)

	def draw(self):
		pygame.draw.circle(self.screen, RED, (self.x, self.y), self.radius)


class Environment:

	def __init__(self, radius, screen):
		self.agents: List[Agent] = []
		self.radius = radius
		self.screen = screen

	def add_boid(self, mouse_x, mouse_y):
		boid = Boid(self.screen, mouse_x, mouse_y, "Boid", self.radius, 1.5708)
		self.agents.append(boid)

	def add_obstacle(self, mouse_x, mouse_y):
		obstacle = Obstacle(self.screen, mouse_x, mouse_y, "Obstacle", self.radius)
		self.agents.append(obstacle)


def init_screen():
	screen = pygame.display.set_mode([750, 750])
	screen.fill((255, 255, 255))
	return screen


# pygame.draw.polygon(screen, RED, draw_triangle(250, 250))
# pygame.draw.aaline(screen, GREEN, [0, 50], [50, 80], True)
# pygame.draw.polygon(screen, GREEN, draw_triangle(250, 250, 11))

# pygame.draw.arc(screen, BLACK, [210, 75, 150, 125], 0, pi / 2, 2)


def quit():
	"""
		Releases resources and quits the game.
	"""
	pygame.quit()
	sys.exit()


def main():
	global elapsed
	global previous

	pygame.init()
	# clock = pygame.time.Clock()
	# main_surface = pygame.display.set_mode(configuration.SCREEN_SIZE)
	# pygame.display.set_caption(configuration.TITLE)

	running = True
	screen = init_screen()
	environment = Environment(radius=10, screen=screen)

	# Used to manage how fast the screen updates
	clock = pygame.time.Clock()

	while running:

		# handle the event
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
				return
			if event.type == pygame.MOUSEBUTTONUP:
				keys = pygame.key.get_pressed()
				if keys[pygame.K_LEFT]:
					mouse = pygame.mouse.get_pos()
					environment.add_boid(mouse[0], mouse[1])
				if keys[pygame.K_RIGHT]:
					mouse = pygame.mouse.get_pos()
					environment.add_obstacle(mouse[0], mouse[1])

				print(pygame.mouse.get_pos())
				print("ce huinea")

		screen.fill(WHITE)
		for agent in environment.agents:
			agent.draw()

		# Fill the background with white

		# Draw a solid blue circle in the center

		# Flip the display
		pygame.display.flip()
		clock.tick(20)


if __name__ == '__main__':
	main()

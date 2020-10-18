import pygame
import sys
from math import pi, cos, sin, sqrt
from typing import List
import math

from hw2.entities.environment import Environment
from hw2.entities.base import Agent
from hw2.entities.agent import Boid
from hw2.common import *

current = None
lag = 0.0
ticks, fps = 0, 0


# configuration = config.GameConfiguration()


def init_screen():
	screen = pygame.display.set_mode([750, 750])
	screen.fill(WHITE)
	return screen


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

		# Flip the display
		pygame.display.flip()
		clock.tick(20)


if __name__ == '__main__':
	main()

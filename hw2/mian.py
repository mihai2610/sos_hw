import pygame
import sys
from hw2.entities.environment import Environment
from hw2.common import *
from random import uniform

current = None
lag = 0.0
ticks, fps = 0, 0


def init_screen():
	screen = pygame.display.set_mode([SCREEN_SIZE, SCREEN_SIZE])
	screen.fill(WHITE)
	return screen


def quit():
	"""
		Releases resources and quits the game.
	"""
	pygame.quit()
	sys.exit()


def main():
	pygame.init()

	running = True
	screen = init_screen()
	environment = Environment(radius=10, screen=screen)

	for i in range(10, SCREEN_SIZE, 20):
		environment.add_obstacle(10, i)
		environment.add_obstacle(SCREEN_SIZE - 10, i)
		environment.add_obstacle(i, SCREEN_SIZE - 10)
		environment.add_obstacle(i, 10)

	for i in range(20):
		environment.add_boid(uniform(0, 750), uniform(0, 750))

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

				print("obstacles_nr = ", environment.obstacle_nr, "boids_nr = ", environment.boid_nr)

		screen.fill(WHITE)

		for agent in environment.agents:
			if agent.name == BOID_NAME:
				agent.update_position(environment.agents)

			agent.draw()

		# Flip the display
		pygame.display.flip()
		clock.tick(20)


if __name__ == '__main__':
	main()

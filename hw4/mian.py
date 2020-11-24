import numpy as np
import math

MAX_ITERATIONS = 500
NR_PARTICLES = 50


class Particle(object):

	def __init__(self, position, velocity, c, w):
		self.position = position
		self.velocity = velocity
		self.c = c
		self.w = w

	def update_position(self, p_best, g_best):
		r = np.random.uniform()

		new_v = self.w * self.velocity + self.c[0] * r * (p_best - self.position) + self.c[1] * r * \
				(g_best - self.position)

		self.velocity = np.array(new_v)
		self.position += self.velocity


class Environment(object):

	def __init__(self, func, nr_particles, init_pos, phi, c, w):
		self.func = func
		self.nr_particles = nr_particles
		self.init_position = np.array(init_pos)
		self.phi = phi
		self.c = c
		self.w = w

		self.particles = [Particle(position, np.random.uniform((2, 2)), self.c, self.w) for position in
						  np.random.uniform(size=(self.nr_particles, 2)) * self.init_position]

		self.g_best = init_pos
		self.p_best = [particle.position for particle in self.particles]

	def optimize(self):

		for iteration in range(MAX_ITERATIONS):
			for (p_index, particle) in enumerate(self.particles):

				p_best = self.p_best[p_index]
				particle.update_position(p_best, self.g_best)

				if self.func(particle.position) < self.func(p_best):
					self.p_best[p_index] = particle.position

				if self.func(particle.position) < self.func(self.g_best):
					self.g_best = particle.position

		return self.g_best, self.func(self.g_best)


def sphere(x):
	return np.sum(np.square(x))


def rosenbrock(X):
	a = 1. - X[0]
	b = X[1] - X[0] * X[0]
	return a * a + b * b * 100.


def rastrigin(X):
	A = 10
	return 2 * A + np.sum([(x ** 2 - A * np.cos(2 * math.pi * x)) for x in X])


def griewank(X):
	_sum = np.sum([x ** 2 for x in X])
	_prod = np.prod([np.cos(x / np.sqrt(i+1)) for (i, x) in enumerate(X)])

	return 1 + (1 / 4000) * _sum - _prod


def main():
	init_pos = [1.5, 1.5]
	phi = []
	c = [0.5, 1.5]
	w = 0.75

	environment = Environment(func=griewank,
							  nr_particles=NR_PARTICLES,
							  init_pos=init_pos,
							  phi=phi,
							  c=c,
							  w=w)

	print(environment.optimize())


if __name__ == '__main__':
	main()

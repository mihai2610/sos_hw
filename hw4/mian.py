import numpy as np
import math
import os

MAX_ITERATIONS = 500
NR_PARTICLES = 25
FILE_PATH = r"D:\master\an2\SOS\sos_hw\hw4\file.csv"

FULL = "FULL"
FOURNEIFG = "FOURNEIFG"
RING = "RING"


class Particle(object):

	def __init__(self, position, velocity, c, w, chi):
		self.position = position
		self.velocity = velocity
		self.c = c
		self.w = w
		self.chi = chi

	def update_position(self, p_best, g_best):
		r1 = np.random.uniform()
		r2 = np.random.uniform()

		new_v = self.w * self.velocity + self.c[0] * r1 * (p_best - self.position)
		new_v += self.c[1] * r2 * (g_best - self.position)
		new_v *= self.chi

		self.velocity = np.array(new_v)
		self.position += self.velocity

	def __str__(self):
		return "({}, {})".format(self.position[0], self.position[1])


class Environment(object):

	def __init__(self, func, nr_particles, init_pos, c, w, chi):
		self.func = func
		self.nr_particles = nr_particles
		self.init_position = np.array(init_pos)
		self.c = c
		self.w = w
		self.chi = chi

		self.particles = [Particle(position, np.random.uniform((2, 2)), self.c, self.w, self.chi) for position in
						  np.random.uniform(size=(self.nr_particles, 2)) * self.init_position]

		self.g_best = [init_pos[0] * 10, init_pos[0] * 10]
		self.p_best = [particle.position.copy() for particle in self.particles]

	def optimize(self, name):
		if name == FULL:
			return self.full_neigh()
		elif name == FOURNEIFG:
			return self.four_neigh()
		elif name == RING:
			return self.ring()
		else:
			raise Exception("Wrong topology")

	def ring(self):

		for iteration in range(MAX_ITERATIONS):
			for (p_index, particle) in enumerate(self.particles):
				next_neigh_index = (p_index + 1) % self.nr_particles
				prev_neigh_index = p_index - 1

				if prev_neigh_index < 0:
					prev_neigh_index = self.nr_particles + prev_neigh_index

				p_best = self.p_best[p_index]

				prev_neigh_val = self.func(self.particles[prev_neigh_index].position)
				next_neigh_val = self.func(self.particles[next_neigh_index].position)
				current_part_val = self.func(particle.position)

				best_val_index = np.argmin([prev_neigh_val, current_part_val, next_neigh_val])
				ring_neighbours = [self.particles[prev_neigh_index], particle, self.particles[next_neigh_index]]
				ring_best_particle = ring_neighbours[best_val_index]

				if self.func(ring_best_particle.position) < self.func(p_best):
					self.p_best[p_index] = particle.position

				if self.func(particle.position) < self.func(self.g_best):
					self.g_best = particle.position

				particle.update_position(p_best, self.g_best)

		return self.g_best, self.func(self.g_best)

	def four_neigh(self):
		sqrt_n = int(np.sqrt(self.nr_particles))

		for iteration in range(MAX_ITERATIONS):
			for (p_index, particle) in enumerate(self.particles):

				n_u = (p_index + sqrt_n) % self.nr_particles
				n_d = p_index - sqrt_n if p_index >= sqrt_n else self.nr_particles - max(p_index, 1)
				n_r = (p_index + 1) % self.nr_particles
				n_l = p_index - 1 if p_index >= 1 else self.nr_particles - 1

				p_best = self.p_best[p_index]

				neigh_particles = [self.particles[n_u], self.particles[n_d], self.particles[n_r], self.particles[n_l]]

				best_particle_index = np.argmin([self.func(p.position) for p in neigh_particles])
				best_particle = neigh_particles[best_particle_index]

				if self.func(best_particle.position) < self.func(p_best):
					self.p_best[p_index] = best_particle.position

				if self.func(particle.position) < self.func(self.g_best):
					self.g_best = particle.position

				particle.update_position(p_best, self.g_best)

		return self.g_best, self.func(self.g_best)

	def full_neigh(self):
		sqrt_n = int(np.sqrt(self.nr_particles))

		for iteration in range(MAX_ITERATIONS):
			for (p_index, particle) in enumerate(self.particles):
				n_u = (p_index + sqrt_n) % self.nr_particles
				n_d = p_index - sqrt_n if p_index >= sqrt_n else self.nr_particles - max(p_index, 1)
				n_r = (p_index + 1) % self.nr_particles
				n_l = p_index - 1 if p_index >= 1 else self.nr_particles - 1

				neighs_index = [
					n_u,
					n_d,
					n_r,
					n_l,
					n_u - 1 if n_u >= 1 else self.nr_particles - 1,
					(n_u + 1) % self.nr_particles,
					n_d - 1 if n_d >= 1 else self.nr_particles - 1,
					(n_d + 1) % self.nr_particles
				]

				neigh_particles = [self.particles[pos] for pos in neighs_index]

				best_particle_index = np.argmin([self.func(p.position) for p in neigh_particles])

				p_best = self.p_best[p_index]

				if self.func(neigh_particles[best_particle_index].position) < self.func(p_best):
					self.p_best[p_index] = neigh_particles[best_particle_index].position

				if self.func(particle.position) < self.func(self.g_best):
					self.g_best = particle.position

				particle.update_position(p_best, self.g_best)

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
	_prod = np.prod([np.cos(x / np.sqrt(i + 1)) for (i, x) in enumerate(X)])

	return 1 + (1 / 4000) * _sum - _prod


def run_experiments():
	init_pos = [1, 1]
	c = [[0.5, 3.5], [0.9, 3.1], [1.0, 3.0]]
	w = [1]
	chi = [0.73]
	functions = [rosenbrock]
	optimizers = [FULL]
	# with open(FILE_PATH, "w") as f:

	for _function in functions:
		print("+++++++++++++++++++++++++++++++++++++++++")
		print("Function = {}".format(_function.__name__))
		print("+++++++++++++++++++++++++++++++++++++++++")
		for _optimizer in optimizers:
			print("\t--------------------------------------")
			print("\tOptimizer = {}".format(_optimizer))
			print("\t--------------------------------------")
			for _c in c:
				for (_chi, _w) in zip(chi, w):
					best_result = 99999999999999999999999
					best_position = [1, 1]

					for i in range(10):
						environment = Environment(func=_function,
												  nr_particles=NR_PARTICLES,
												  init_pos=init_pos,
												  c=_c,
												  w=_w,
												  chi=_chi)

						result = environment.optimize(_optimizer)

						if result[1] < best_result:
							best_result = result[1]
							best_position = result[0]
					print("\t\t c = {}, _chi = {}, w = {} coordinates = {} best result = {}".format(_c, _chi, _w,
																									best_position,
																									best_result))

						# f.write("{},{},{},{},{},{},{},{},{}\n".format(_function.__name__, _optimizer, _c[0], _c[1], _w,
						# 											  _chi, best_position[0], best_position[1],
						# 											  best_result))


def main():
	# init_pos = [1, 1]
	# c = [0.5, 1.5]
	# w = 0.75
	# chi = 1
	#
	# environment = Environment(func=griewank,
	# 						  nr_particles=NR_PARTICLES,
	# 						  init_pos=init_pos,
	# 						  c=c,
	# 						  w=w,
	# 						  chi=chi)
	#
	# print(environment.optimize(RING))
	print(sphere([1, 1]))
	print(rosenbrock([1, 1]))
	print(rastrigin([1, 1]))
	print(griewank([1, 1]))


if __name__ == '__main__':
	# main()
	run_experiments()

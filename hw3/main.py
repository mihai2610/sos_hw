from typing import List
import numpy as np
import random
from itertools import permutations
from hw3.Environment import Environment
import math

import tsp

params = [
	[1., 3., 0.99],
	[1., 3., 0.5],
	[1., 5., 0.99],
	[1., 5., 0.5],
	[1., 8., 0.99],
	[1., 8., 0.5],
	[0.5, 5., 0.99],
	[0.5, 5., 0.5],
]


def calculate_path_cost(graph, path):
	cost = 0
	costs = ""
	for i in range(len(path) - 1):
		costs += " " + str(graph[path[i]][path[i + 1]])
		cost += graph[path[i]][path[i + 1]]

	print(costs)
	return cost


def generate_graph(nr_nodes: int) -> List[List[int]]:
	_graph = np.zeros((nr_nodes, nr_nodes))

	for k in range(nr_nodes):
		for i in range(k, nr_nodes):
			for j in range(k, nr_nodes):
				if i != j:
					_graph[i, j] = _graph[j, i] = random.randrange(1, 30)

	return _graph


def print_graph(graph: List[List[int]], nr_nodes: int) -> None:
	for i in range(nr_nodes):
		to_print = ""
		for j in range(nr_nodes):
			to_print += " {:.2f}".format(graph[i][j])

		print(to_print)


def calculate_base_tsp(graph: List[List[int]], source_node: int) -> (List[int], int):
	nr_nodes = len(graph)

	nodes_list = np.arange(nr_nodes)

	all_paths = permutations(nodes_list)

	global_cost = 9999999999
	global_path = []

	for path in all_paths:
		if path[0] == source_node:
			local_cost = 0
			y = source_node

			for index in range(nr_nodes - 1):
				x = path[index]
				y = path[index + 1]

				local_cost += graph[x][y]

			if local_cost < global_cost:
				global_cost = local_cost
				global_path = np.copy(path)

	return global_path, global_cost


def ants_optimized_pts(environment: Environment, max_iterations: int) -> (List[int], int):
	while max_iterations > 0:
		max_iterations -= 1

		environment.step()

	# print("++++++++++++++++++++++++++++++++++++++++++++")
	# print_graph(environment.pheromone_graph, nr_nodes=len(environment.graph))
	# print("++++++++++++++++++++++++++++++++++++++++++++")

	return environment.global_min_path, environment.global_min_cost, environment.source_node


def main():
	nr_nodes = 9
	source_node = 0
	nr_ants = 5
	max_iterations = 1000

	alpha = 1.
	beta = 3.
	ro = 0.99

	graph = generate_graph(nr_nodes)

	print_graph(graph, nr_nodes)

	environment = Environment(nr_nodes=nr_nodes,
							  source_node=source_node,
							  nr_ants=nr_ants,
							  max_iterations=max_iterations,
							  graph=graph,
							  alpha=alpha,
							  beta=beta,
							  ro=ro)

	print("alpha | beta  | ro  | optimal  | optimized  | avg_optimized | diff ")

	for param in params:
		environment.alpha = param[0]
		environment.beta = param[1]
		environment.ro = param[2]

		base_costs = []
		base_paths = []

		optimized_costs = []
		optimized_paths = []

		for i in range(10):
			environment.pheromone_graph = np.ones((nr_nodes, nr_nodes))

			optimized_path, optimized_cost, source_node = ants_optimized_pts(environment, max_iterations)
			# print(optimized_path)
			# print(optimized_cost)

			optimized_costs.append(optimized_cost)
			optimized_paths.append(optimized_path)

			base_path, base_cost = calculate_base_tsp(graph, environment.source_node)
			# print(base_path)
			# print(base_cost)

			base_costs.append(base_cost)
			base_paths.append(base_path)

		# print("alpha = {} | beta = {} | ro = {} | optimal = {} | optimized = {} | diff = {} "
		# 	  .format(alpha, beta, ro, base_cost, optimized_cost, abs(base_cost - optimized_cost)))

		best_base_cost = np.min(base_costs)
		best_base_path = base_paths[np.argmin(base_costs)]

		best_optimized_cost = np.min(optimized_costs)
		best_optimized_path = optimized_paths[np.argmin(optimized_costs)]

		# print("best_optimized = ", calculate_path_cost(graph, best_optimized_path))
		# print("best_base = ", calculate_path_cost(graph, best_base_path))

		avg_optimized_cost = np.sum(optimized_costs) / len(optimized_costs)
		diff = abs(best_base_cost - best_optimized_cost)

		# print("alpha = {} | beta = {} | ro = {} | optimal = {} | optimized = {} | avg_optimized = {} | diff = {} "
		# 	  .format(environment.alpha, environment.beta, environment.ro, best_base_cost, best_optimized_cost,
		# 			  avg_optimized_cost, diff))

		print("{} {} {} {} {} {} {} ".format(environment.alpha, environment.beta, environment.ro, best_base_cost,
											 best_optimized_cost, avg_optimized_cost, diff))



if __name__ == '__main__':
	main()

from typing import List, Tuple
import numpy as np
from hw3.Agent import Agent
from hw3.Common import Observation
import random


class Environment(object):

	def __init__(self, nr_nodes: int,
				 source_node: int,
				 nr_ants: int,
				 max_iterations: int,
				 graph: List[List[int]],
				 alpha: float,
				 beta: float,
				 ro: float):

		self.alpha = alpha
		self.beta = beta
		self.ro = ro

		self.max_iterations = max_iterations
		self.nr_nodes = nr_nodes
		self.nr_ants = nr_ants
		self.ant_pheromone_level = .10

		self.graph = graph
		self.pheromone_graph = np.ones((nr_nodes, nr_nodes))

		self.global_min_cost = sum(graph[0]) + graph[nr_nodes - 1][source_node]
		self.global_min_path = np.append(np.arange(nr_nodes), source_node)
		self.source_node = source_node

	# self.agents = [Agent(source_node, self.ant_pheromone_level, self.alpha, self.beta, self.ro) for i in range(self.nr_ants)]

	def step(self):
		updates = []
		agents = [Agent(random.randint(0, self.nr_nodes - 1), self.ant_pheromone_level, self.alpha, self.beta, self.ro)
				  for i in range(self.nr_ants)]
		agents_completed = 0
		min_cost_agent = agents[0]

		while agents_completed < len(agents):
			for agent in agents:
				observations = []
				for i in range(self.nr_nodes):
					observation = Observation(i, self.graph[agent.position][i], self.pheromone_graph[agent.position][i])
					observations.append(observation)

				current_position, next_position, pheromone, completed = agent.action(observations)
				agents_completed += completed

				if completed == 0:
					update = [current_position, next_position, pheromone]
					updates.append(update)
				else:
					if min_cost_agent.cost > agent.cost:
						min_cost_agent = agent

			for update in updates:
				self.pheromone_graph[update[0]][update[1]] = update[2]
				self.pheromone_graph[update[1]][update[0]] = update[2]

		self.global_min_cost = min_cost_agent.cost
		self.global_min_path = min_cost_agent.visited_nodes
		self.source_node = min_cost_agent.source

		for i in range(self.nr_nodes - 1, 1, -1):
			source = min_cost_agent.visited_nodes[i]
			destination = min_cost_agent.visited_nodes[i - 1]

			update_value = (1 - self.alpha) * (self.pheromone_graph[source][destination]) + self.alpha / self.nr_nodes
			self.pheromone_graph[source][destination] += update_value
			self.pheromone_graph[destination][source] = self.pheromone_graph[source][destination]

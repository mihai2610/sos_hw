from typing import List, Tuple
import random
from hw3.Common import Observation
import numpy as np


class Agent(object):

	def __init__(self, source: int,
				 pheromone_0: float,
				 alpha: float,
				 beta: float,
				 ro: float):
		self.alpha = alpha
		self.beta = beta
		self.ro = ro

		self.source = source
		self.position = source
		self.pheromone_0 = pheromone_0
		self.visited_nodes = []
		self.cost = 0

	def action(self, neighbours: List[Observation]):

		self.visited_nodes.append(self.position)

		not_visited = [neighbour for neighbour in neighbours if
					   (neighbour.node_id != self.position and neighbour.node_id not in self.visited_nodes)]

		not_visited_len = len(not_visited)

		if not_visited_len == 0:
			return self.position, self.source, 0., 1
		else:
			neighbour_prob = dict()
			down = np.sum([(nb.pheromone ** self.alpha * (1/nb.cost) ** self.beta) for nb in not_visited])

			for neighbour in not_visited:
				up = (neighbour.pheromone ** self.alpha * (1/neighbour.cost) ** self.beta)
				neighbour_prob[neighbour.node_id] = up / down

			next_nb_node_id = np.random.choice(list(neighbour_prob.keys()), p=list(neighbour_prob.values()))
			next_neighbour = [nb for nb in not_visited if nb.node_id == next_nb_node_id][0]

		update_pheromone = (1. - self.ro) * next_neighbour.pheromone + (self.ro * self.pheromone_0)
		old_position = self.position

		self.cost += next_neighbour.cost
		self.position = next_neighbour.node_id

		return old_position, self.position, update_pheromone, 0

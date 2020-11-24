class Observation(object):
	def __init__(self, node_id: int, cost: int, pheromone: float):
		self.node_id = node_id
		self.cost = cost
		self.pheromone = pheromone

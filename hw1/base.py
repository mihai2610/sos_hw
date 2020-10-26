from typing import List


class Agent(object):
	"""
	Base class to be implemented by agent implementations. A reactive agent is only defined by its Agent @ to
	perceptions.
	"""

	def __init__(self, x: int, y: int, name: str = None):
		if not name:
			self.name = "*A"
		else:
			self.name = name

		self.x = x
		self.y = y
		self.value = 1

	def response(self, perception: List[List[object]]) -> int:
		raise NotImplementedError("Missing a response")

	def __str__(self):

		return "{} : x = {}, y = {}, value = {}".format(self.name, self.x, self.y, self.value)

	def __hash__(self):
		return hash(self.name + str(self.x) + str(self.y))


class Environment(object):
	"""
	Base class to be implemented by environment implementations.
	"""

	def add_agent(self, agent: Agent, x: int, y: int):
		raise NotImplementedError("Method not implemented")

	def step(self) -> bool:
		raise NotImplementedError("Method not implemented")

	def __str__(self):
		raise NotImplementedError("Method not implemented")

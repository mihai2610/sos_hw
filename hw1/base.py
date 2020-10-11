from typing import List


class Action(object):
	"""
	Base class to be implemented by classes representing actions.
	"""
	pass


class Perception(object):
	"""
	Base class to be implemented by classes representing the totality of an agent's perceptions at a point in time.
	"""
	pass


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
		"""
		Supplies the agent with perceptions and demands one action from the agent. The environment also specifies if the
		previous action of the agent has succeeded or not.

		:param perception: the perceptions offered by the environment to the agent.
		:return: he agent output, containing the action to perform. Action should be of type
		{@link blocksworld.BlocksWorldAction.Type#NONE} if the agent is not performing an action now,
		but may perform more actions in the future.
		Action should be of type {@link blocksworld.BlocksWorldAction.Type#AGENT_COMPLETED} if the agent will not
		perform any more actions ever in the future.
		"""
		raise NotImplementedError("Missing a response")

	def __str__(self):
		"""
		:return: The agent name
		"""
		return "{} : x = {}, y = {}, value = {}".format(self.name, self.x, self.y, self.value)

	def __hash__(self):
		return hash(self.name + str(self.x) + str(self.y))


class Environment(object):
	"""
	Base class to be implemented by environment implementations.
	"""

	def add_agent(self, agent: Agent, x: int, y: int):
		"""
		Adds an agent to the environment. The environment places the agent in it, in the specified state.
		:param agent: the agent to add.
		:param x: row position of the agent
		:param y: column position of the agent
		"""
		raise NotImplementedError("Method not implemented")

	def step(self) -> bool:
		"""
		When the method is invoked, all agents should receive a perception of the environment and decide on an action to
		perform.
		:return: True if all agents completed their goals
		"""
		raise NotImplementedError("Method not implemented")

	def __str__(self):
		raise NotImplementedError("Method not implemented")

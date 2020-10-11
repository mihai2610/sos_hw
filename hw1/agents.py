from hw1.base import Agent
from typing import List


class PascalAgent(Agent):

	def __init__(self, x: int, y: int, name: str = None):
		super(PascalAgent, self).__init__(name=name, x=x, y=y)

	def response(self, perception: List[List[Agent]]) -> int:

		if self.y == 0 or self.y == self.x:
			return self.value

		left_value = perception[self.x - 1][self.y - 1].value
		right_value = perception[self.x - 1][self.y].value

		return left_value + right_value

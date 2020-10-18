from hw1.base import Agent, Environment
from hw1.agents import PascalAgent
from typing import Callable, List

class PascalEnvironment(Environment):

	def __init__(self, n_rows: int):
		stack: List[List[PascalAgent]] = []

		for i in range(n_rows):
			row = [PascalAgent(i, index) for index in range(i + 1)]
			stack.append(row)

		self.stack: List[List[PascalAgent]] = stack
		self.n_rows = n_rows

	def add_agent(self, agent: PascalAgent, x: int, y: int):
		agent_name = "Agent_{}_{}".format(x, y)
		self.stack[x][y] = PascalAgent(x, y, agent_name)

	def step(self) -> bool:
		new_values = dict(dict())
		updates = False

		for row in self.stack:
			for col in row:

				new_value = col.response(self.stack)

				if new_value != col.value:
					if col.x not in new_values.keys():
						new_values[col.x] = dict()

					new_values[col.x][col.y] = new_value
					updates = True

		if updates:
			for row_key in new_values.keys():
				for col_key in new_values[row_key].keys():
					self.stack[row_key][col_key].value = new_values[row_key][col_key]

			return True

		return False

	def __str__(self):
		result = ""

		for i in range(self.n_rows):
			result += str([str(agent.value) for agent in self.stack[i]]) + "\n"

		return result


if __name__ == '__main__':
	n = 8
	pascal_env = PascalEnvironment(n_rows=n)

	next_step = True
	max_num_steps = 10000

	while next_step and max_num_steps > 0:
		next_step = pascal_env.step()
		max_num_steps -= 1

	print(pascal_env)

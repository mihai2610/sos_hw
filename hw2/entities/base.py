class Agent(object):

	def __init__(self, screen, x: float, y: float, name: str, radius: float = 2):
		self.x = x
		self.y = y
		self.radius = radius
		self.name = name
		self.screen = screen

	def __str__(self):
		return "Agent {} : ({}, {})".format(self.name, self.x, self.y)

	def draw(self):
		raise NotImplementedError

import strategies
import cards

class player:
	def __init__(self, name, money, strategy):
		self.name = name
		self.money = int(money)
		self.strategy = strategies.get_strategy(strategy)
		self.cards = []
		self.fold = False

	def decide(self):
		return self.strategy.decide(self.cards)

	def reset_state(self):
		self.cards = []
		self.fold = False

	def __str__(self):
		return self.name

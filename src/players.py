import strategies
import cards

class Player:
	def __init__(self, name, money, prev_player, next_player):
		self.name = name
		self.money = int(money)
		self.cards = []
		# now property 'fold' is replaced by 'current_stake is None'
		self.stake = 0
		self.prev = prev_player
		self.next = next_player

	# def decide(self):
	# 	return self.strategy.decide(self.cards)

	def reset_state(self):
		self.cards = []
		self.stake = 0

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.name

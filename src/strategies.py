import random

basic_ = 0
advanced_ = 1
random_ = 2

responses = ['raise', 'call', 'check', 'fold', 'all-in']

# TODO: rename to 'get'
def get_strategy(strategy):
	if strategy == basic_ or strategy == 'basic':
		return basic_strategy()
	elif strategy == advanced_ or strategy == 'advanced':
		return advanced_strategy()
	elif strategy == random_ or strategy == 'random':
		return random_strategy()
	else:
		return basic_strategy()

class basic_strategy:
	def __init__(self):
		self.name = 'basic'

	def __repr__(self):
		return self.name

	def decide(self, cards):
		return ('check', 0)	# temporary action

class advanced_strategy:
	def __init__(self):
		self.name = 'advanced'

	def __repr__(self):
		return self.name

	def decide(self, cards):
		return ('raise', 50)	# temporary action

class random_strategy:
	def __init__(self):
		self.name = 'random'

	def __repr__(self):
		return self.name

	def decide(self, cards):
		decision = random.choice(responses)
		# we don't want to go all-in too frequently
		if (decision == 'all-in'):
			decision = random.choice(responses)
		return (decision, 10)	# temporary action
		

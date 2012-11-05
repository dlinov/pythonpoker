import random

basic_ = 0
advanced_ = 1
random_ = 2

responses = ['raise', 'call', 'check', 'fold', 'all-in']

def get_strategy(strategy):
	if strategy == basic_:
		return basic_strategy()
	elif strategy == advanced_:
		return advanced_strategy()
	elif strategy == random_:
		return random_strategy()
	else:
		return basic_strategy()

class basic_strategy:
	def __init__(self):
		self.name = 'basic'

	def decide(self, cards):
		return ('check', 0)	# temporary action

class advanced_strategy:
	def __init__(self):
		self.name = 'advanced'

	def decide(self, cards):
		return ('raise', 50)	# temporary action

class random_strategy:
	def __init__(self):
		self.name = 'random'

	def decide(self, cards):
		decision = random.choice(responses)
		# we don't want to go all-in too frequently
		if (decision == 'all-in'):
			decision = random.choice(responses)
		return (decision, 10)	# temporary action
		

import poker

def get(strategy_class):
	"""
	strategy_class can be 'basic', 'advanced', 'random'
	"""
	print('{} selected as data'.format(strategy_class))
	if strategy_class == 'basic':
		return basic_processing()
	else:
		print("{}-processing hasn't implemented yet".format(strategy_class))

class basic_processing(object):
	def __init__(self):
		self.name = 'basic'

	def __repr__(self):
		return self.name

	def decide(self, game_state):
		# temporary action
		result = []
		if game_state.need_decision:
			print('DEBUG: taking decision...')
			game_state.need_decision = False
			result.append(('fold', 0))
		return result
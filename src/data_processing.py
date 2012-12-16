import poker
import cards

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
		# need to check if input can differ check and call
		result = []
		if game_state.need_decision:
			print('DEBUG: taking decision...')
			game_state.need_decision = False
			decision = None
			if game_state.stage == poker.stages.preflop:
				decision = self.analyze_preflop(game_state)
			elif game_state.stage == poker.stages.flop:
				decision = self.analyze_flop(game_state)
			elif game_state.stage == poker.stages.turn:
				decision = self.analyze_turn(game_state)
			elif game_state.stage == poker.stages.river:
				decision = self.analyze_river(game_state)

			if decision:
				result.append(decision)
		return result

	def analyze_preflop(self, game_state):
		result = None
		bank = game_state.bank
		my_stack = game_state.player.money
		if bank and my_stack:
			# all-in if player has small stack
			if bank / my_stack > 8:
				result = 'raise'
			else:
				my_cards = game_state.player.cards
				c1 = my_cards[0]; c2 = my_cards[1]
				my_max_val = max([lambda c: cards.values.index(c), my_cards])
				if c1.suit == c2.suit:
					print('DEBUG: you have the same suits, so raise')
					result = 'raise'
				elif c1.val == c2.val:
					print('DEBUG: you have a pair, so raise')
					result = 'raise'
				elif my_max_val >= cards.values.index('10'):
					result = 'raise' if my_max_val >= cards.values.index('Q') else 'check'
				else:
					result = 'fold'
		else:
			result = 'check'
		return result

	def analyze_flop(self, game_state):
		result = None
		bank = game_state.bank
		my_stack = game_state.player.money
		if my_stack:
			result = 'check'
			## all-in if player has small stack
			#if bank / my_stack > 8:
			#	result = 'raise'
			#else:
			#	my_cards = game_state.player.cards
			#	c1 = my_cards[0]; c2 = my_cards[1]
			#	my_max_val = max([lambda c: cards.values.index(c), my_cards])
			#	if c1.suit == c2.suit:
			#		print('DEBUG: you have the same suits, so raise')
			#		result = 'raise'
			#	elif c1.val == c2.val:
			#		print('DEBUG: you have a pair, so raise')
			#		result = 'raise'
			#	elif my_max_val >= cards.values.index('10'):
			#		result = 'raise' if my_max_val >= cards.values.index('Q') else 'check'
			#	else:
			#		result = 'fold'
		else:
			result = 'check'
		return result

	def analyze_turn(self, game_state):
		result = None
		bank = game_state.bank
		my_stack = game_state.player.money
		if my_stack:
			result = 'check'
			## all-in if player has small stack
			#if bank / my_stack > 8:
			#	result = 'raise'
			#else:
			#	my_cards = game_state.player.cards
			#	c1 = my_cards[0]; c2 = my_cards[1]
			#	my_max_val = max([lambda c: cards.values.index(c), my_cards])
			#	if c1.suit == c2.suit:
			#		print('DEBUG: you have the same suits, so raise')
			#		result = 'raise'
			#	elif c1.val == c2.val:
			#		print('DEBUG: you have a pair, so raise')
			#		result = 'raise'
			#	elif my_max_val >= cards.values.index('10'):
			#		result = 'raise' if my_max_val >= cards.values.index('Q') else 'check'
			#	else:
			#		result = 'fold'
		else:
			result = 'check'
		return result

	def analyze_river(self, game_state):
		result = None
		bank = game_state.bank
		my_stack = game_state.player.money
		if my_stack:
			result = 'check'
			## all-in if player has small stack
			#if bank / my_stack > 8:
			#	result = 'raise'
			#else:
			#	my_cards = game_state.player.cards
			#	c1 = my_cards[0]; c2 = my_cards[1]
			#	my_max_val = max([lambda c: cards.values.index(c), my_cards])
			#	if c1.suit == c2.suit:
			#		print('DEBUG: you have the same suits, so raise')
			#		result = 'raise'
			#	elif c1.val == c2.val:
			#		print('DEBUG: you have a pair, so raise')
			#		result = 'raise'
			#	elif my_max_val >= cards.values.index('10'):
			#		result = 'raise' if my_max_val >= cards.values.index('Q') else 'check'
			#	else:
			#		result = 'fold'
		else:
			result = 'check'
		return result

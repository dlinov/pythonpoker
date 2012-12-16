import poker
import cards

def get(strategy_class):
	"""
	strategy_class can be 'basic', 'advanced', 'random'
	"""
	print('{} selected as data'.format(strategy_class))
	if strategy_class == 'basic':
		return BasicProcessing()
	else:
		print("{}-processing hasn't implemented yet".format(strategy_class))

class BasicProcessing(object):
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
			hand = poker.recognize_hand(game_state.player.cards, game_state.table_cards)
			card_set = game_state.player.cards + game_state.table_cards			
			if game_state.can_check:
				# check or raise
				flush_len = 4
				flush_possibility = poker.check_flush(card_set, flush_len)
				# pair or better or 4 cards of the same suit		
				if hand[0] > 0 or flush_possibility:
					result = 'bet'
				else:
					result = 'check'
			else:
				flush_len = 2
				flush_possibility = poker.check_flush(card_set, flush_len)
				if flush_possibility:
					result = 'fold'
				elif hand[0] > 1:	# two pairs or better
					result = 'raise'
				else:
					result = 'call'
		else:
			result = 'check'
		return result

	def analyze_turn(self, game_state):
		result = None
		bank = game_state.bank
		my_stack = game_state.player.money
		if my_stack:
			hand = poker.recognize_hand(game_state.player.cards, game_state.table_cards)
			card_set = game_state.player.cards + game_state.table_cards	
			if game_state.can_check:
				if hand[0] > 2:
					result = 'bet'
				else:
					result = 'check'
			else:
				better_than_two_pairs = hand[0] > 2
				better_than_three_of_a_kind = hand[0] > 3
				better_than_flush = hand[0] > 5
				# change, need to recognize if pair lies on the table
				pair_of_q_or_higher = hand[0] > 1 and max(lambda c: cards.values.index(c), cards) > 9
				flush_len = 3
				flush_possibility = poker.check_flush(card_set, flush_len)
				if flush_possibility:
					if better_than_flush:
						result = 'call'
					else:
						result = 'fold'
				else:
					if better_than_flush:
						result = 'raise'
					else:
						if better_than_three_of_a_kind:
							result = 'call'
						else:
							result = 'fold'
		else:
			result = 'check'
		return result

	def analyze_river(self, game_state):
		result = None
		bank = game_state.bank
		my_stack = game_state.player.money
		if my_stack:
			hand = poker.recognize_hand(game_state.player.cards, game_state.table_cards)
			card_set = game_state.player.cards + game_state.table_cards	
			if game_state.can_check:
				if hand[0] > 3:
					result = 'bet'
				else:
					result = 'check'
			else:
				better_than_two_pairs = hand[0] > 2
				better_than_three_of_a_kind = hand[0] > 3
				better_than_flush = hand[0] > 5
				# change, need to recognize if pair lies on the table
				pair_of_q_or_higher = hand[0] > 1 and max(lambda c: cards.values.index(c), cards) > 9
				flush_len = 4
				flush_possibility = poker.check_flush(card_set, flush_len)
				if flush_possibility:
					if better_than_flush:
						result = 'call'
					else:
						result = 'fold'
				else:
					if better_than_flush:
						result = 'raise'
					else:
						if better_than_three_of_a_kind:
							result = 'call'
						else:
							result = 'fold'
		else:
			result = 'check'
		return result

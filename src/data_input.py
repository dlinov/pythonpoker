import cards
import players
import poker

def get(input_class):
	"""
	source_kind can be 'console', 'gui'
	output_kind can be 'console', 'gui'
	"""
	print('{} selected as input'.format(input_class))
	if input_class == 'console':
		return input_console()
	else:
		print("{}-input hasn't implemented yet".format(input_class))

# TODO: create new source file for each class
class input_console:
	def __init__(self):
		pass

	def __repr__(self):
		return 'console input'

	def reset_state_round(self, game_state):
		game_state.round_reset()

	def reset_state_game(self, game_state):
		game_state = game_state()

	def get_state(self, game_state):
		if game_state.stage == poker.stages.game_start:
			# here we need to define player details, opponents number and start money
			self.process_start_game(game_state)
		elif game_state.stage == poker.stages.nocards:
			# here we need to enter two player's cards
			self.process_nocards(game_state)
		elif game_state.stage == poker.stages.preflop:
			self.process_preflop(game_state)
		elif game_state.stage == poker.stages.flop:
			self.process_flop(game_state)
		elif game_state.stage == poker.stages.turn:
			self.process_turn(game_state)
		elif game_state.stage == poker.stages.river:
			self.process_river(game_state)
		elif game_state.stage == poker.stages.showdown:
			self.process_showdown(game_state)
		else:
			print('ERROR: stage not recognized')

	def get_card(self):
		''' input format - [value, suit], e.g. "2H" or "AD" '''
		try:
			card_code = input('Enter card:')
			v_index = 1 if card_code[:2] != '10' else 2
			# get first elem from enumeration
			suit = next(st for st in filter(lambda s: s.startswith(str.lower(card_code[v_index:])), cards.suits) if st)
			value = card_code[:v_index]
			return cards.card(suit, value)
		except:
			print('ERROR: card input cannot be parsed')
			return self.get_card()

	def process_start_game(self, game_state):
		inp = input('enter your name: ')
		selfname = inp if inp != '' else 'Dmitry'
		inp = input('enter start amount of money: ')
		start_money = int(inp if inp.isdigit() else '10')
		game_state.player = players.player(selfname, start_money, None)
		inp = input('enter opponents number: ')
		num = int(inp if inp.isdigit() else '1')
		for i in range(0, num):
			name = input('enter opponent #{0} name: '.format(i + 1))
			# TODO: remove strategy parameter from player constructor
			p = players.player(name if name != '' else 'enemy{}'.format(i), start_money, None)
			print('player {} with start money = {} added'.format(p, start_money))
			game_state.opponents.append(p)
		game_state.stage = poker.stages.nocards

	def process_nocards(self, game_state):
		game_state.player.cards.append(self.get_card())
		game_state.player.cards.append(self.get_card())
		game_state.stage = poker.stages.preflop

	def process_preflop(self, game_state):
		# TODO: take stakes from all players then step to flop
		# self.input.get_stakes()
		game_state.stage = poker.stages.game_over
		pass

	def process_flop(self, game_state):
		# TODO: take stakes from all players then step to turn
		game_state.stage = poker.stages.game_over
		pass

	def process_turn(self, game_state):
		# TODO: take stakes from all players then step to river
		game_state.stage = poker.stages.game_over
		pass

	def process_river(self, game_state):
		# TODO: take stakes from all players then step to showdown
		game_state.stage = poker.stages.game_over
		pass

	def process_showdown(self, game_state):
		# TODO: take stakes from all players then start new round or end game
		game_state.stage = poker.stages.game_over
		pass
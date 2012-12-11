import cards
import players
import poker
import cross_py_func as crf
import img_func as imf
import threading
import os

def get(input_class):
	"""
	source_kind can be 'console', 'gui'
	"""
	print('{} selected as input'.format(input_class))
	if input_class == 'console':
		return input_console()
	if input_class == 'gui':
		return input_gui()
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
		result = None
		while not result:
			try:
				card_code = crf.readline('Enter card: ')
				v_index = 1 if card_code[:2] != '10' else 2
				# get first elem from enumeration
				suit = next(st for st in filter(lambda s: s.startswith(str.lower(card_code[v_index:])), cards.suits) if st)
				value = card_code[:v_index]
				result = cards.card(suit, value)
			except:
				print('ERROR: card input cannot be parsed')
		return result

	def get_stakes(self, game_state):
		"""universal method to get stakes at various round stages"""
		# get players who has bet less than needed
		without_stake = list(filter(lambda p: p.stake < game_state.bank_part, filter(lambda y: y, game_state.players)))

		cycle_label = game_state.last_bet_by.next
		current = cycle_label

		while current.next is not cycle_label:			
			# if current player is not fold
			if current.stake >= 0:
				game_state.last_bet_by = current
				if current is game_state.player:
					# return process game state				
					return
				else:
					# get other players' stakes
						d = crf.readline("Enter {}'s decision (f[old], c[heck/all], r[aise]/b[et], a[ll-in]: ".format(current)) 
						if d.startswith('f'):
							current.stake = None
						elif d.startswith('c'):
							# check or call - autocall if you can't check
							diff = game_state.bank_part - current.stake
							current.money -= diff
							current.stake += diff
						elif d.startswith('r') or d.startswith('b'):
							# raise or bet
							# by default, bet is equal to blind + difference between required and current bank_part
							# may be the 2nd input for stake should be implemented
							diff = current.money - (game_state.bank_part - current.stake + game_state.blind)
							if (diff < 0):
								print("WARNING: get_stakes, diff is less than zero. Maybe it's all-in player")
							else:
								bet = game_state.blind if diff >= game_state.blind else diff
								game_state.bank_part += bet
								cycle_label = current	# cycle starts_again
						elif d.startswith('a'):
							# all-in
							diff = current.money - (game_state.bank_part - current.stake)
							current.money = 0
							game_state.bank_part += diff
						else:
							print('ERROR: wrong input')
			else:
				print('DEBUG: {} is fold'.format(current))
			current = current.next
		return True

	def process_start_game(self, game_state):
		inp = crf.readline('enter start amount of money: ')
		start_money = int(inp if inp.isdigit() else '100')
		inp = crf.readline('enter blind: ')
		game_state.blind = int(inp if inp.isdigit() else '10')

		inp = crf.readline('enter player number: ')
		num = int(inp if inp.isdigit() else '2')
		if num < 2:
			print('WARNING: player number should be greater or equal to 2. Player is set to 2')
			num = 2

		user_flag = False
		for i in range(0, num):
			inp = crf.readline('enter opponent #{0} name: '.format(i + 1))
			name = inp if inp != '' else 'player{}'.format(i)
			prev = game_state.players[i - 1] if i > 0 else None
			p = players.player(name , start_money, prev, None)
			if not user_flag:
				inp = crf.readline('enter "+" if this player is you: ')
				user_flag = inp == '+'
				if user_flag:
					game_state.player = p
			if prev:
				prev.next = p
			game_state.players.append(p)
			print('player "{}" with start money = {} added'.format(p, start_money))

		game_state.players[0].prev = game_state.players[-1]
		game_state.players[-1].next = game_state.players[0]

		game_state.small_blind = game_state.players[0]
		game_state.big_blind = game_state.players[1]
		game_state.stage = poker.stages.nocards

	def process_nocards(self, game_state):
		game_state.round_reset()
		while (len(game_state.player.cards) < 2):
			game_state.player.cards.append(self.get_card())
		game_state.stage = poker.stages.preflop

	def process_preflop(self, game_state):
		# TODO: take stakes from all players then step to flop
		end_stage = self.get_stakes(game_state)
		if end_stage:
			game_state.stage = poker.stages.flop

	def process_flop(self, game_state):
		# TODO: take stakes from all players then step to turn
		if (len(game_state.table_cards) != 3):
			game_state.table_cards.append(self.get_card())
			game_state.table_cards.append(self.get_card())
			game_state.table_cards.append(self.get_card())
			print('DEBUG: table on flop: {}'.format(game_state.table_cards))
		end_stage = self.get_stakes(game_state)
		if end_stage:
			game_state.stage = poker.stages.turn

	def process_turn(self, game_state):
		# TODO: take stakes from all players then step to river
		if (len(game_state.table_cards) != 4):
			game_state.table_cards.append(self.get_card())
			print('DEBUG: table on turn: {}'.format(game_state.table_cards))
		end_stage = self.get_stakes(game_state)
		if end_stage:
			game_state.stage = poker.stages.river

	def process_river(self, game_state):
		# TODO: take stakes from all players then step to showdown
		if (len(game_state.table_cards) != 5):
			game_state.table_cards.append(self.get_card())
			print('DEBUG: table on river: {}'.format(game_state.table_cards))
		end_stage = self.get_stakes(game_state)
		if end_stage:
			game_state.stage = poker.stages.showdown

	def process_showdown(self, game_state):
		print('DEBUG: table on showdown: {}'.format(game_state.table_cards))
		for p in game_state.players:
			if p.stake is not None:
				print('DEBUG: {}\'s cards: {}'.format(p, p.cards))
			else:
				print('DEBUG: {} is fold'.format(p))

		# TODO: choose winner(s)

		game_state.players = list(filter(lambda p: p.money > 0, game_state.players))
		if (len(game_state.players) < 2):
			print('WINNER IS {}'.format(game_state.players[0]))
			game_state.stage = poker.stages.game_over
		else:
			game_state.stage = poker.stages.nocards

class input_gui:
	def __init__(self):
		self.path_to_cards = '..\\img\\cards'
		self.path_to_test = '..\\img\\test'
		self.path_to_markers = '..\\img\\markers'
		self.path_to_buttons = '..\\img\\buttons'

	def __repr__(self):
		return 'graphic input'

	def get_state(self, game_state):
		# Remember player pos (l/r)
		# try to recognize 7 cards
		# found 2 - preflop
		# found 5 - flop
		# found 6 - turn
		# found 7 - river or showdown
		# recognize 'fold' button - if recognized, we call AI for decision
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

	def get_marker_location(self):
		path = os.path.join(self.path_to_markers, 'hand_16_40.png')
		# TODO: call it several times
		self.marker = imf.get_marker_location(path)
		print('Marker supposed to be at {}'.format(self.marker))

	def reset_state_round(self, game_state):
		game_state.round_reset()

	def reset_state_game(self, game_state):
		game_state = game_state()

	def get_card(self, offset):
		result = None
		try:
			x1, y1, x2, y2 = self.marker + offset
			card_code = imf.get_card((x1 + x2, y1 + y2))
			#card_code = crf.readline('Enter card: ')
			v_index = 1 if card_code[:2] != '10' else 2
			# get first elem from enumeration
			suit = next(st for st in filter(lambda s: s.startswith(str.lower(card_code[v_index:])), cards.suits) if st)
			value = card_code[:v_index]
			result = cards.card(suit, value)
		except:
			print('ERROR: card input cannot be parsed')
		return result

	def contains_button(self, button_text, offset):
		path = os.path.join(self.path_to_buttons, button_text + '.png')
		x1, y1, x2, y2 = self.marker + offset
		return imf.contains_button(path, (x1 + x2, y1 + y2))


	#def get_stakes(self, game_state):
	#	"""universal method to get stakes at various round stages"""
	#	# get players who has bet less than needed
	#	without_stake = list(filter(lambda p: p.stake < game_state.bank_part, filter(lambda y: y, game_state.players)))

	#	cycle_label = game_state.last_bet_by.next
	#	current = cycle_label

	#	while current.next is not cycle_label:			
	#		# if current player is not fold
	#		if current.stake >= 0:
	#			game_state.last_bet_by = current
	#			if current is game_state.player:
	#				# return process game state				
	#				return
	#			else:
	#				# get other players' stakes
	#					d = crf.readline("Enter {}'s decision (f[old], c[heck/all], r[aise]/b[et], a[ll-in]: ".format(current)) 
	#					if d.startswith('f'):
	#						current.stake = None
	#					elif d.startswith('c'):
	#						# check or call - autocall if you can't check
	#						diff = game_state.bank_part - current.stake
	#						current.money -= diff
	#						current.stake += diff
	#					elif d.startswith('r') or d.startswith('b'):
	#						# raise or bet
	#						# by default, bet is equal to blind + difference between required and current bank_part
	#						# may be the 2nd input for stake should be implemented
	#						diff = current.money - (game_state.bank_part - current.stake + game_state.blind)
	#						if (diff < 0):
	#							print("WARNING: get_stakes, diff is less than zero. Maybe it's all-in player")
	#						else:
	#							bet = game_state.blind if diff >= game_state.blind else diff
	#							game_state.bank_part += bet
	#							cycle_label = current	# cycle starts_again
	#					elif d.startswith('a'):
	#						# all-in
	#						diff = current.money - (game_state.bank_part - current.stake)
	#						current.money = 0
	#						game_state.bank_part += diff
	#					else:
	#						print('ERROR: wrong input')
	#		else:
	#			print('DEBUG: {} is fold'.format(current))
	#		current = current.next
	#	return True	

	def process_start_game(self, game_state):
		self.get_marker_location()
		#region test
		card1 = self.get_card((46, 169))
		print(card1)
		card2 = self.get_card((61, 173))
		print(card2)
		card3 = self.get_card((263, 175))
		print(card3)
		card4 = self.get_card((317, 175))
		print(card4)
		card5 = self.get_card((371, 175))
		print(card5)
		card6 = self.get_card((425, 175))
		print(card6)
		card7 = self.get_card((479, 175))
		print(card7)
		card8 = self.get_card((672, 170))
		print(card8)
		card9 = self.get_card((687, 174))
		print(card9)
		print(self.contains_button('fold', (378, 480)))
		print(self.contains_button('check', (514, 480)))
		#endregion
		# TODO: remove hardcode
		game_state.blind = 2

		game_state.stage = poker.stages.nocards

	#inp = crf.readline('enter start amount of money: ')
	#start_money = int(inp if inp.isdigit() else '100')
	#inp = crf.readline('enter blind: ')
	#game_state.blind = int(inp if inp.isdigit() else '10')

	#inp = crf.readline('enter player number: ')
	#num = int(inp if inp.isdigit() else '2')
	#if num < 2:
	#	print('WARNING: player number should be greater or equal to 2. Player is set to 2')
	#	num = 2

	#user_flag = False
	#for i in range(0, num):
	#	inp = crf.readline('enter opponent #{0} name: '.format(i + 1))
	#	name = inp if inp != '' else 'player{}'.format(i)
	#	prev = game_state.players[i - 1] if i > 0 else None
	#	p = players.player(name , start_money, prev, None)
	#	if not user_flag:
	#		inp = crf.readline('enter "+" if this player is you: ')
	#		user_flag = inp == '+'
	#		if user_flag:
	#			game_state.player = p
	#	if prev:
	#		prev.next = p
	#	game_state.players.append(p)
	#	print('player "{}" with start money = {} added'.format(p, start_money))

	#game_state.players[0].prev = game_state.players[-1]
	#game_state.players[-1].next = game_state.players[0]

	#game_state.small_blind = game_state.players[0]
	#game_state.big_blind = game_state.players[1]
	#game_state.stage = poker.stages.nocards

	def process_nocards(self, game_state):
		game_state.round_reset()
		while (len(game_state.player.cards) < 2):
			game_state.player.cards.append(self.get_card())
		game_state.stage = poker.stages.preflop

	def process_preflop(self, game_state):
		# TODO: take stakes from all players then step to flop
		end_stage = self.get_stakes(game_state)
		if end_stage:
			game_state.stage = poker.stages.flop

	def process_flop(self, game_state):
		# TODO: take stakes from all players then step to turn
		if (len(game_state.table_cards) != 3):
			game_state.table_cards.append(self.get_card())
			game_state.table_cards.append(self.get_card())
			game_state.table_cards.append(self.get_card())
			print('DEBUG: table on flop: {}'.format(game_state.table_cards))
		end_stage = self.get_stakes(game_state)
		if end_stage:
			game_state.stage = poker.stages.turn

	def process_turn(self, game_state):
		# TODO: take stakes from all players then step to river
		if (len(game_state.table_cards) != 4):
			game_state.table_cards.append(self.get_card())
			print('DEBUG: table on turn: {}'.format(game_state.table_cards))
		end_stage = self.get_stakes(game_state)
		if end_stage:
			game_state.stage = poker.stages.river

	def process_river(self, game_state):
		# TODO: take stakes from all players then step to showdown
		if (len(game_state.table_cards) != 5):
			game_state.table_cards.append(self.get_card())
			print('DEBUG: table on river: {}'.format(game_state.table_cards))
		end_stage = self.get_stakes(game_state)
		if end_stage:
			game_state.stage = poker.stages.showdown

	def process_showdown(self, game_state):
		print('DEBUG: table on showdown: {}'.format(game_state.table_cards))
		for p in game_state.players:
			if p.stake is not None:
				print('DEBUG: {}\'s cards: {}'.format(p, p.cards))
			else:
				print('DEBUG: {} is fold'.format(p))

		# TODO: choose winner(s)

		game_state.players = list(filter(lambda p: p.money > 0, game_state.players))
		if (len(game_state.players) < 2):
			print('WINNER IS {}'.format(game_state.players[0]))
			game_state.stage = poker.stages.game_over
		else:
			game_state.stage = poker.stages.nocards


import cards
from game_state import game_state

def get(input_class):
	print('{} selected as input'.format(input_class))
	if input_class == 'console':
		return input_console()
	else:
		print("{}-input hasn't implemented yet".format(input_class))

# TODO: create new source file for each class
class input_console:
	def __init__(self):
		self.reset_state_game()

	def reset_state_round(self):
		self.state.round_reset()

	def reset_state_game(self):
		self.state = game_state()

	def get_state(self):
		if self.state.stage == 'start_game':
			# here we need to enter players number and start money
			self.process_start_game()
			pass
		if self.state.stage == 'nocards':
			# here we need to enter two player's cards
			self.process_nocards()
			pass
		elif self.state.stage == 'preflop':
			pass
		elif self.state.stage == 'flop':
			pass
		elif self.state.stage == 'turn':
			pass
		elif self.state.stage == 'river':
			pass
		elif self.state.stage == 'showdown':
			pass
		else:
			print('ERROR: stage not recognized')

		return self.state

	def get_card(self):
		''' input format - [value, suit], e.g. "2H" or "AD" '''
		card_code = input('Enter card:')
		suit = filter(lambda s: s[0] == card_code.to_lower()[1], cards.suits)
		value = card_code[0]
		return card(suit, value)

	def process_start_game(self):		
		start_money = int(input('enter start amount of money: '))

		num = int(input('enter opponents number: '))
		for i in range(0, num):
			name = input('enter opponent #{0} name: '.format(i + 1))
			# TODO: remove strategy parameter from player constructor
			p = players.player(name, start_money, None)
			self.state.opponents.append(p)
		print('=== players added ===')

	def process_nocards(self):		
		card1 = self.get_card()
		print(card1)
		card2 = self.get_card()
		print(card2)
		self.state.player_cards.append(card1)
		self.state.player_cards.append(card1)
		# TODO: change for:
		# self.state.player_cards.append(get_card())
		# self.state.player_cards.append(get_card())
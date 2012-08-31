import random
import cards
import players

class table:
	def __init__(self):
		self.deck = cards.deck()
		self.open_cards = []
		self.players = []
		self.bank = 0
		self.s_blind = 1	# small blind money value
		self.b_blind = 2	# big blind money value
		self.blind_indices = {'small': 0, 'big': 1}	# blind player indices

	def take_new_deck(self):
		self.deck = cards.deck()
		self.open_cards = []
		for p in self.players:
			p.reset_state()

	def add_player(self, player):
		self.players.append(player)

	def move_blinds(self):
		# choosing of small blind
		while int(self.players[self.blind_indices['small']].money) < self.s_blind:
			print('DEBUG: ' + self.players.pop(self.blind_indices['small']).name + ' was deleted as (s)he hasn\'t enough money to be the small blind')			
			if self.blind_indices['small'] == len(self.players):
				self.blind_indices['small'] = 0

		self.blind_indices['big'] = self.blind_indices['small'] + 1
		print('DEBUG: After choosing small blind blinds are: ' + str(self.blind_indices))

		# choosing of big blind
		while int(self.players[self.blind_indices['big']].money) < self.b_blind:
			if self.blind_indices['big'] == self.blind_indices['small']:
				# may be check for one player and infinite loop
				self.blind_indices['big'] = (self.blind_indices['big'] + 1) % len(self.players)
			else:
				print('DEBUG: ' + self.players.pop(self.blind_indices['big']).name + ' was deleted as (s)he hasn\'t enough money to be the big blind')
				if self.blind_indices['small'] > self.blind_indices['big']:
					# test!
					self.blind_indices['small'] += 1
				if self.blind_indices['big'] == len(self.players):
					self.blind_indices['big'] = 0

		print('DEBUG: Small blind is: ' + self.players[self.blind_indices['small']].name)
		print('DEBUG: Big blind is: ' + self.players[self.blind_indices['big']].name)


	def take_blinds(self):
		if len(self.players) < 2:
			print('DEBUG: add more players')
			return # raise
		else:
			self.players[self.blind_indices['small']].money -= self.s_blind
			self.players[self.blind_indices['big']].money -= self.b_blind
			self.bank = self.s_blind + self.b_blind

	def trade(self):
		for p in self.players:
			if not p.fold:
				decision = p.decide()	# need o transfer more information
				print(p.name + '\'s decision: ' + str(decision))

	def show_flop(self):
		for i in range(1, 4):
			self.open_cards.append(self.deck.pop())

		print('flop: ' + str(self.open_cards))

	def show_turn(self):
		self.open_cards.append(self.deck.pop())

		print('turn: ' + str(self.open_cards))

	def show_river(self):
		self.open_cards.append(self.deck.pop())

		print('river: ' + str(self.open_cards))

	def finish_round(self):
		# choose round winner
		winners = choose_winners(self.players, self.open_cards)
		print('Round winner(s): {0}'.format(winners))

		winners_count = len(winners)
		for w in winners:
			w.money += self.bank / winners_count
		self.bank = 0


def choose_winners(players, river):
	intermediate_winners = [players[0]]
	intermediate_hand = recognize_hand(intermediate_winners[0].cards, river)

	for p in players[1:]:	# comparing all player hands to intermediate best hand
		current_hand = recognize_hand(p.cards, river)
		if current_hand > intermediate_hand:	
			intermediate_winners = list(p)
			intermediate_hand = current_hand
		elif current_hand == intermediate_hand:
			intermediate_winners.append(p)

	return intermediate_winners

def recognize_hand(hand, river):
	cards = hand + river
	print('DEBUG: hand recognition. Cards:\n{0}'.format(cards))

	# number of combination. Higher is better. Royal flush is 8, high card is 0
	combination = 8

	# check_* functions return high card of combination or None if there is no desired combination
	high_card = check_royal_flash(cards)
	if not high_card:
		combination -= 1 								# 7
		high_card = check_4_of_a_kind(cards)
		if not high_card:
			combination -= 1							# 6
			high_card = check_full_house(cards)
			if not high_card:
				combination -= 1						# 5
				high_card = check_flush(cards)
				if not high_card:
					combination -= 1					# 4
					high_card = check_straight(cards)
					if not high_card:
						combination -= 1				# 3
						high_card = check_3_of_a_kind(cards)
						if not high_card:
							combination -= 1			# 2
							high_card = check_2_pairs(cards)
							if not high_card:
								combination -= 1		# 1
								high_card = check_pair(cards)
								if not high_card:
									combination -= 1	# 0

	return (combination, high_card)

def check_royal_flash(cards):
	pass

def check_4_of_a_kind(cards):
	pass

def check_full_house(cards):
	pass

def check_flush(cards):
	pass

def check_straight(cards):
	pass

def check_3_of_a_kind(cards):
	pass

def check_2_pairs(cards):
	pass

def check_pair(cards):
	pass






		

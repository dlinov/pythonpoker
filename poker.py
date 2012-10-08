import random
import cards
import players

class table:
	def __init__(self):
		self.deck = cards.deck()
		self.open_cards = []
		self.players = []
		self.bank = 0
		self.s_blind = 2							# small blind money value
		self.b_blind = 4							# big blind money value
		self.blinds = {'small': None, 'big': None}	# blind player indices

	def take_new_deck(self):
		self.deck = cards.deck()
		self.open_cards = []
		for p in self.players:
			p.reset_state()

	def add_player(self, player):
		self.players.append(player)

	def next_player_for(self, player):
		'''Returns next player for another one. If he doesn't exist in the collection, returns first element if collection'''
		n = len(self.players)
		if n < 1:
			raise

		index = 0
		if player in self.players:
			index = (self.players.index(player) + 1) % n

		return self.players[index]

	# should it raise exception when len(self.players) < 2?
	def move_blinds(self):
		old_sb = self.blinds['small']

		# search of players with non-positive balance
		players_to_remove = list(filter(lambda p: p.money <= 0, self.players))
		print('DEBUG: players with non-positive balance: {}'.format(players_to_remove))

		# removing invalid players
		for p in players_to_remove:
			# if current SB player hasn't money, move SB to the next position
			if self.blinds['small'] == p:
				self.blinds['small'] = self.next_player_for(p)

			self.players.remove(p)

		print('DEBUG: players after filtering: {}'.format(self.players))

		# choosing of small blind
		# if SB hasn't moved during filtering
		if old_sb == self.blinds['small']:
			self.blinds['small'] = self.next_player_for(self.blinds['small'])

		# choosing of big blind
		self.blinds['big'] = self.next_player_for(self.blinds['small'])

		print('DEBUG: Small blind is: {}'.format(self.blinds['small']))
		print('DEBUG: Big blind is: ' + self.blinds['big'].name)

	# TODO: check rules what happens when player has less money then needed for his blind
	def take_blinds(self):
		if len(self.players) < 2:
			print('DEBUG: add more players')
			return # raise
		else:
			small_part = self.s_blind if self.blinds['small'].money >= self.s_blind else self.blinds['small'].money
			big_part = self.b_blind if self.blinds['big'].money >= self.b_blind else self.blinds['big'].money

			self.blinds['small'].money -= small_part
			self.blinds['big'].money -= big_part
			self.bank = small_part + big_part

	def trade(self):
		# TODO: filter
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
		# TODO: check rules what happens when winning is fractional number
		winning = self.bank // winners_count
		for w in winners:
			w.money += winning
		self.bank = 0

		for p in self.players:
			print('{}: {}'.format(p.name, p.money))


def choose_winners(players, river):
	intermediate_winners = []
	intermediate_hand = (-1, None)	# (combination, high card)

	for p in players:	# comparing all player hands
		current_hand = recognize_hand(p.cards, river)
		print('{}\'s hand power: {}'.format(p, current_hand))
		if current_hand > intermediate_hand:	
			intermediate_winners = [p]
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

def check_royal_flash(card_set):
	pass

def check_4_of_a_kind(card_set):
	pass

def check_full_house(card_set):
	'''three of a kind + pair'''
	pass

def check_flush(card_set):
	'''5 or more cards of the same suit'''
	suits = [card.suit for card in card_set]

	for suit in cards.suits:
		n = len(list(filter(lambda s: s == suit, suits)))
		if n >= 5:
			return True

	return False
	pass

def check_straight(card_set):
	pass

def check_3_of_a_kind(card_set):
	pass

def check_2_pairs(card_set):
	pass

def check_pair(card_set):
	pass
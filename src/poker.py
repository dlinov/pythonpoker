import random
import cards
import players
from collections import namedtuple

# game_start - the very beginning of the game - we need to know names and start amount of money
# nocards - no one has cards
# preflop - everyone has two cards
# flop - three cards are opened
# turn - four cards are opened
# river - five cards are opened
# showdown - opening player's cards
_s = namedtuple('stages', ['game_start', 'nocards', 'preflop', 'flop', 'turn', 'river', 'showdown', 'game_over'])
stages = _s('game start', 'no cards', 'preflop', 'flop', 'turn', 'river', 'showdown', 'game over')

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
		###
		filtered_players = list(filter(lambda p: not p.fold, self.players))
		if len(filtered_players) > 1:
			for p in filtered_players:
				if not p.fold:
					decision = p.decide()	# need to transfer more information	
					word = decision[0]
					if word == 'fold':			
						p.fold = True
					if word == 'all-in':
						self.bank += p.money
						p.money = 0
					###/
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

		winners_count = len(winners)
		if winners_count > 0:
			# TODO: check rules what happens when winning is fractional number
			winning = self.bank // winners_count
			print('Round winner(s): {}. Each won: {}'.format(winners, winning))
			for w in winners:
				w.money += winning
		else:
			print('No winner. Improve strategies :)')		
		self.bank = 0

		for p in self.players:
			print('{}: {}'.format(p.name, p.money))

class game_state:
	def __init__(self):
		# is needed only to remember fields
		self.player = None
		self.table_cards = []
		self.players = []
		self.opponents = self.get_opponents
		self.stage = stages.game_start
		self.small_blind = None
		self.big_blind = None
		self.blind = 0
		self.last_bet_by = None
		self.bank = 0
		self.bank_part = 0	# amount of money, every player's part of bank to match
		self.need_decision = False

	def get_opponents(self):
		opponents = list(self.players)
		if self.player in self.players:
			opponents.remove(self.player)
		return opponents

	def round_reset(self):
		"""Resets bank, player hands and takes money from blinds"""
		for p in self.players: p.reset_state()
		#self.player = player(self.player.name, self.player.cards)
		self.small_blind.money -= self.blind // 2
		self.small_blind.stake += self.blind // 2
		self.big_blind.money -= self.blind
		self.big_blind.stake += self.blind
		self.last_bet_by = self.big_blind
		self.bank = self.blind
		self.bank_part = self.blind
		self.table_cards = []
		self.stage = stages.nocards

def choose_winners(players, river):
	intermediate_winners = []
	intermediate_hand = (-1, None)	# (combination, high card)
	print('DEBUG: choosing winners. Number of active players: {}'.format(len(list(filter(lambda p: not p.fold, players)))))

	for p in players:	# comparing all player hands
		if not p.fold:
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

	# check_[name of combination] functions return combination order
	# and 
	# combination cards set or None if there is no desired combination
	best_hand = check_straight_flash(cards)
	if not best_hand:
		combination -= 1 								# 7
		best_hand = check_4_of_a_kind(cards)
		if not best_hand:
			combination -= 1							# 6
			best_hand = check_full_house(cards)
			if not best_hand:
				combination -= 1						# 5
				best_hand = check_flush(cards)
				if not best_hand:
					combination -= 1					# 4
					best_hand = check_straight(cards)
					if not best_hand:
						combination -= 1				# 3
						best_hand = check_three_of_a_kind(cards)
						if not best_hand:
							combination -= 1			# 2
							best_hand = check_two_pairs(cards)
							if not best_hand:
								combination -= 1		# 1
								best_hand = check_pair(cards)
								if not best_hand:
									combination -= 1	# 0

	return (combination, best_hand)

def check_straight_flash(card_set):
	return None

def check_4_of_a_kind(card_set):
	values = [card.val for card in card_set]

	for val in cards.values:
		res_hand = list(filter(lambda v: v == val, values))
		n = len(res_hand)
		if n >= 4:
			return True
	return None

def check_full_house(card_set):
	'''three of a kind + pair'''
	three = check_three_of_a_kind(card_set)

	if three:
		new_card_set = list(card_set)
		# for item in three:
		# 	new_card_set.remove(item)
		# pair = check_pair(new_card_set)
		# TODO: return other values
		# return True if pair else None
		
	return None

def check_flush(card_set):
	'''5 or more cards of the same suit'''
	suits = [card.suit for card in card_set]

	for suit in cards.suits:
		n = len(list(filter(lambda s: s == suit, suits)))
		if n >= 5:
			return True
	return None

def check_straight(card_set):
	'''5 cards in a row by value'''
	values = [card.val for card in card_set]
	check_list = list(cards.values)
	check_list.insert(0, 'A')
	n = 0

	for item in check_list:
		if item in values:
			n += 1
			if (n >= 5):
				return True
		else:
			n = 0

	return None

def check_three_of_a_kind(card_set):
	'''3 cards of the same value'''
	values = [card.val for card in card_set]

	for val in cards.values:
		n = len(list(filter(lambda v: v == val, values)))
		if n >= 3:
			return True
	return None

def check_two_pairs(card_set):
	'''2 pairs'''
	values = [card.val for card in card_set]
	pairs_number = 0;
	for val in cards.values:
		n = len(list(filter(lambda v: v == val, values)))
		if n >= 2:
			pairs_number += 1
	return pairs_number >= 2

def check_pair(card_set):
	'''one pair'''
	values = [card.val for card in card_set]

	for val in cards.values:
		n = len(list(filter(lambda v: v == val, values)))
		if n >= 2:
			return True
	return None
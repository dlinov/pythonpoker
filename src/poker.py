from collections import namedtuple
import itertools
import random
import itertools
import cards
import players

# game_start - the very beginning of the game - we need to know names and start amount of money
# nocards - no one has cards
# preflop - everyone has two cards
# flop - three cards are opened
# turn - four cards are opened
# river - five cards are opened
# showdown - opening player's cards
_s = namedtuple('stages', ['game_start', 'nocards', 'preflop', 'flop', 'turn', 'river', 'showdown', 'game_over'])
stages = _s('game start', 'no cards', 'preflop', 'flop', 'turn', 'river', 'showdown', 'game over')

class Table:
	def __init__(self):
		self.deck = cards.Deck()
		self.open_cards = []
		self.players = []
		self.bank = 0
		self.s_blind = 2							# small blind money value
		self.b_blind = 4							# big blind money value
		self.blinds = {'small': None, 'big': None}	# blind player indices

	def take_new_deck(self):
		self.deck = cards.Deck()
		self.open_cards = []
		for p in self.players:
			p.reset_state()

	def add_player(self, player):
		self.players.append(player)

	def next_player_for(self, player):
		'''Returns next player for another one. If he doesn't exist in the collection, returns first element of collection'''
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

class GameState:
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
		self.can_check = False

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
			# current_hand = recognize_hand(p.cards, river)
			current_hand = best_hand(p.cards + river)
			print('{}\'s hand power: {}'.format(p, current_hand))
			if current_hand > intermediate_hand:	
				intermediate_winners = [p]
				intermediate_hand = current_hand
			elif current_hand == intermediate_hand:
				intermediate_winners.append(p)
	return intermediate_winners

def best_hand(hand):
	"From a 7-card hand, return the best 5 card hand."
	combs = list(itertools.combinations(hand, 5))
	combs.sort(reverse = True, key = hand_rank)
	return combs[0]

def hand_rank(hand):
	"Return a value indicating the ranking of a hand."
	ranks = card_ranks(hand) 
	if straight(ranks) and flush(hand):
		return (8, max(ranks))
	elif kind(4, ranks):
		return (7, kind(4, ranks), kind(1, ranks))
	elif kind(3, ranks) and kind(2, ranks):
		return (6, kind(3, ranks), kind(2, ranks))
	elif flush(hand):
		return (5, ranks)
	elif straight(ranks):
		return (4, max(ranks))
	elif kind(3, ranks):
		return (3, kind(3, ranks), ranks)
	elif two_pair(ranks):
		return (2, two_pair(ranks), ranks)
	elif kind(2, ranks):
		return (1, kind(2, ranks), ranks)
	else:
		return (0, ranks)

def card_ranks(hand):
	"Return a list of the ranks, sorted with higher first."
	ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
	ranks.sort(reverse = True)
	return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks

def flush(hand):
	"Return True if all the cards have the same suit."
	suits = [s for r,s in hand]
	return len(set(suits)) == 1

def straight(ranks):
	"""Return True if the ordered 
	ranks form a 5-card straight."""
	return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5

def kind(n, ranks):
	"""Return the first rank that this hand has 
	exactly n-of-a-kind of. Return None if there 
	is no n-of-a-kind in the hand."""
	for r in ranks:
		if ranks.count(r) == n: return r
	return None

def two_pair(ranks):
	"""If there are two pair here, return the two 
	ranks of the two pairs, else None."""
	pair = kind(2, ranks)
	lowpair = kind(2, list(reversed(ranks)))
	if pair and lowpair != pair:
		return (pair, lowpair)
	else:
		return None

import random

# clubs = '♣'
# diamonds = '♦'
# hearts = '♥'
# spades = '♠'
suits = (['clubs', 'diamonds', 'hearts', 'spades'])

values = (['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'])

class card:
	def __init__(self, suit, val):
		if (suit in suits or str(val) in values):
			self.suit = suit
			self.val =  str(val)	# store value as string even if a number was transfered
		else:
			print('check cards.suits and/or cards.values')
			self = None
		

	def __str__(self):
		if self: 
			return "{0}{1}".format(self.val, self.suit)
		else:
			return 'none'

	def __repr__(self):
		if self:
			return "{0} of {1}".format(self.val, self.suit)
		else:
			return 'none'

class deck:
	def __init__(self):
		self.cards = [card(suit, val) for suit in suits for val in values]
		self.is_shuffled = False

	def shuffle(self):
		random.shuffle(self.cards)
		self.is_shuffled = True

	def pop(self):
		if self.is_shuffled is False:
			print('WARNING: deck is not shuffled.')
		if len(self.cards) == 0:
			return None
		else:
			return self.cards.pop() # pops last elem in sequence. 
import cards

class manual:
	def __init__(self):
		self.cards = []

	def enter_card(self, card_code):
		''' input format - [value, suit], e.g. "2H" or "AD" '''
		suit = filter(lambda s: s[0] == card_code.to_lower()[1], cards.suits)
		value = card_code[0]
		card = card(suit, value)
		self.cards.append(card)

	def clear_cards(self):
		self.cards.clear()

class winapi:
	pass

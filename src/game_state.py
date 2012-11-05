import cards
import players

class game_state:
	# game_start - the very beginning of the game - we need to know names and start amount of money
	# nocards - no one has cards
	# preflop - everyone has two cards
	# flop - three cards are opened
	# turn - four cards are opened
	# river - five cards are opened
	# showdown - opening player's cards
	stages = ('game_start' 'nocards', 'preflop', 'flop', 'turn', 'river', 'showdown')

	def __init__(self):
		# is needed only to remember fields
		self.player = None
		self.table_cards = []
		self.opponents = []
		self.stage = 'game_start'

	def round_reset(self):
		self.player = player(self.player.name, self.player.cards)
		# TODO: update opponents
		self.table_cards = []
		self.stage = 'nocards'
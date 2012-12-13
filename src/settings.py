import json
import pickle
import poker

class settings:
	def __init__(self):
		self.player0_cards_pos = (((46, 169)), (61, 173))
		self.player0_bank_offset = (44, 265, 104, 275)
		self.player1_cards_pos = ((672, 170), (687, 174))		
		self.player1_bank_offset = (674, 265, 734, 275)
		self.table_cards_pos = ((263, 175), (317, 175), (371, 175), (425, 175), (479, 175))
		self.buttons = {'fold': (378, 480), 'check': (514, 480)}		
		self.path_to_cards = '..\\img\\cards'
		self.path_to_test = '..\\img\\test'
		self.path_to_markers = '..\\img\\markers'
		self.path_to_buttons = '..\\img\\buttons'
		self.marker_main_name = 'hand_16_40.png'
import data_input
import data_output

class manager:
	def __init__(self, src, out):
		self.input = data_input.get(src)
		self.output = data_output.get(out)

# class input:
# 	def __init__(self, source_kind, output_kind):
# 		"""
# 		source_kind can be 'console', 'gui'
# 		output_kind can be 'console', 'gui'
# 		"""
# 		# TODO: need to specify way to choose input: manual, image, etc.
# 		self.source = data_input()
# 		# self.state

# 	def get_state(self):
# 		state = game_state()
# 		if source is not None:
# 			state.player_balance = source.get_player_balance()
# 			state.player_cards = source.get_player_cards()
# 			state.table_cards = source.get_table_cards()
# 			state.opponents = source.get_opponents()

# 		return state

# class output:
# 	pass

import data_input	# all inputs
import data_output	# all outputs
import poker		# rules, game state

class manager:
	def __init__(self, src, out):
		self.input = data_input.get(src)
		self.output = data_output.get(out)
		self.game_state = poker.game_state()

	def __repr__(self):
		return '{} - {}'.format(self.input, self.output)

	def start(self):
		if self.game_state.stage == poker.stages.game_start:
			print('=== game is starting ===')
			while self.game_state.stage is not poker.stages.game_over:
				print('DEBUG: current stage is: {}'.format(self.game_state.stage))
				self.input.get_state(self.game_state)	# receive current state
				# actions = self.process_current_state()	# process it with AI
				# self.output.do(actions)					# react
			print('=== game finished ===')
		else:
			print('You should finish current game to start a new one')

	def process_current_state(self):
		inp = self.input
		inp.process_nocards()
		self.is_game_active = False

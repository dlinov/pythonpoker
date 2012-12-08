import data_input				# all inputs
import data_output				# all outputs
import data_processing			# all AI
import poker					# rules, game state
import cross_py_func as crf 	# cross-python function implementations

class manager:
	def __init__(self, src, out, ai):
		self.input = data_input.get(src)
		self.output = data_output.get(out)
		self.ai = data_processing.get(ai)
		self.game_state = poker.game_state()

	def __repr__(self):
		return '{} - {} [AI: {}]'.format(self.input, self.output, self.ai)

	def start(self):
		if self.game_state.stage == poker.stages.game_start:
			print('=== game is starting ===')
			while self.game_state.stage is not poker.stages.game_over:
				print('DEBUG: current stage is: {}'.format(self.game_state.stage))
				self.input.get_state(self.game_state)		# receive current state
				actions = self.ai.decide(self.game_state)	# process it with AI
				self.output.do(actions)						# react
			print('=== game finished ===')
		else:
			print('You should finish current game to start a new one')
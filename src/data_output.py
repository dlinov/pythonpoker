import strategies

def get(output_class):
	"""
	output_kind can be 'console', 'gui'
	"""
	print('{} selected as output'.format(output_class))
	if output_class == 'console':
		return output_console()
	else:
		print("{}-output hasn't implemented yet".format(output_class))

# TODO: create new source file for each class
class output_console:
	def __init__(self):
		self.__name__ = 'console output'
		pass

	def __repr__(self):
		return self.__name__
	
	# TODO: implement
	def do(self, actions):
		if actions:
			print('DEBUG: output of decisions')
			for a in actions:
				print(a)
import strategies

def get(output_class):	
	print('{} selected as output'.format(output_class))
	if output_class == 'console':
		return output_console()
	else:
		print("{}-output hasn't implemented yet".format(output_class))

# TODO: create new source file for each class
class output_console:
	def __init__(self):
		pass
	
	# TODO: implement
	def out(self):
		print('Implement decisions')
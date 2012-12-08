import sys

def readline(message):
	version = sys.version_info
	inp = ''
	if version < (3, 0):
		inp = raw_input(message)		
	else:
		inp = input(message)
	return inp
from img_func import get_marker_location
from math import sqrt
import os
import random
import settings
import time
from pymouse import PyMouse

def get(output_class):
	"""
	output_kind can be 'console', 'gui'
	"""
	print('{} selected as output'.format(output_class))
	if output_class == 'console':
		return OutputConsole()
	elif output_class == 'gui':
		return OutputGui()
	else:
		print("{}-output hasn't implemented yet".format(output_class))

# TODO: create new source file for each class
class OutputBase:
	def __repr__(self):
		return self.__name__
	
	def do(self, actions):
		if actions:
			print('DEBUG: output of decisions')
			for a in actions:
				print(a)
				if a == 'check' or a == 'call':
					self.check_or_call(a)
				elif a == 'bet' or a == 'raise':
					self.bet_or_raise(a)
				elif a == 'fold':
					self.fold()
				else:
					print('ERROR: action not recognized: {}'.format(a))

	def check_or_call(self, action):
		raise NotImplementedError

	def bet_or_raise(self, action):
		raise NotImplementedError

	def fold(self):
		raise NotImplementedError

class OutputConsole(OutputBase):
	def __init__(self):
		self.__name__ = 'console output'	
	
	def check_or_call(self, action):
		print(action)

	def bet_or_raise(self, action):
		print(action)

	def fold(self):
		print('fold')

class OutputGui(OutputBase):
	def __init__(self):
		self.__name__ = 'gui output'
		self.mouse = PyMouse()
		self.s = settings.Settings()
	
	def check_or_call(self, action):
		x, y = self.s.buttons['check']
		#x += self.x0; y += self.y0
		self.move_and_click((x, y))

	def bet_or_raise(self, action):		
		x, y = self.s.buttons['raise']
		#x += self.x0; y += self.y0
		self.move_and_click((x, y))

	def fold(self):		
		x, y = self.s.buttons['fold']
		print('DEBUG: fold pos: {}'.format((x, y)))
		#x += self.x0; y += self.y0
		print('DEBUG: absolute fold pos: {}'.format((x, y)))
		self.move_and_click((x, y))

	def move_and_click(self, pos, button = 1): 
		"""
		button: 1 - left; 2 - middle; 3 - right
		"""	
		self.x0, self.y0 = get_marker_location(os.path.join(self.s.path_to_markers, self.s.marker_main_name))
		print('DEBUG: marker (in output): {}'.format((self.x0, self.y0)))
		## move to any position
		#screen_res = self.mouse.screen_size()
		#self.mouse.move(random.randint(0, screen_res[0]), random.randint(0, screen_res[1]))
		#time.sleep(random.random()) # max one second

		# TODO:uncomment in release - simulating of thinking
		#time(sleep(random.randint(1, 7) + random.random())

		# random choosing of moving params: steps, base sleep timeout
		n_steps = random.randint(200, 300)
		print('steps={}'.format(n_steps))
		step_time_base =  random.randint(1, 4) / 400.0
		print('step_time_base={}'.format(step_time_base))
		dest_x, dest_y = pos
		dest_x += self.x0 + 60; dest_y += self.y0 + 25	# to click closer to the button centre
		print('dest={};{}'.format(dest_x, dest_y))
		x0, y0 = self.mouse.position()
		print('start={};{}'.format(x0, y0))
		delta_x = dest_x - x0
		delta_y = dest_y - y0
		print('delta={};{}'.format(delta_x, delta_y))
		dx = float(delta_x) / n_steps
		dy = float(delta_y) / n_steps
		print('dx={}; dy={}'.format(dx, dy))

		for i in xrange(1, n_steps + 1):			
			time.sleep(step_time_base + random.random() / 400)
			# with random devation from destination
			try:
				curr_x, curr_y = self.mouse.position()
				self.mouse.move(int(curr_x + dx + ((random.random() - 0.5) * dx * 4)), int(curr_y + dy + ((random.random() - 0.5) * dy * 4)))
			except:
				print('ERROR: canot move: {}th step'.format(i))

			# exactly destination
			#self.mouse.move(int(x0 + dx * i), int(y0 + dy * i))

		x, y = self.mouse.position()
		while self.deviation(x, y, dest_x, dest_y) > 4:
			try:
				x = int((dest_x + x) / 2)
				y = int((dest_y + y) / 2)
				self.mouse.move(x, y)
			except:
				print('ERROR: cannot reduce deviation. Now is {}'.format(self.deviation(x, y, dest_x, dest_y)))
				break

		print('DEBUG: result = {}. deviation from given position is {}'.format((x, y), self.deviation(x, y, dest_x, dest_y)))		
		time.sleep(1.5)
		self.mouse.move(int(dest_x), int(dest_y))
		time.sleep(0.5)	
		self.mouse.click(int(dest_x), int(dest_y), button)

		# to prevent button highlighting
		self.mouse.move(int(self.x0), int(self.y0))

	def deviation(self, x, y, x0, y0):
		return sqrt((x - x0) ** 2 + (y - y0) ** 2)



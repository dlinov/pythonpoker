from PySide import QtCore

def say_hello(name):
	print ("Hello,", name)

class Foo(QtCore.QObject):
	@QtCore.Slot(str)
	def say_bye(self, name):
		print ("Bye,", name)

class Bar(QtCore.QObject):
	signal = QtCore.Signal(tuple)

f = Foo()
b = Bar()
b.signal.connect(say_hello)
b.signal.connect(f.say_bye)
b.signal.emit("User.")
b.signal.emit(1.25)
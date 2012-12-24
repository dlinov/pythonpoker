import data_io
import cross_py_func as crf

io = data_io.Manager('gui', 'gui', 'basic')
print('IO: {}'.format(io))

crf.readline('press return to start game:')

io.start()
crf.readline('press return to close')


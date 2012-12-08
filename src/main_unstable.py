import data_io
import strategies
import cross_py_func as cr_func

io = data_io.manager('console', 'console')
ai = strategies.get_strategy('basic')
print('IO: {}; AI: {}'.format(io, ai))

cr_func.readline('press return to start game:')

io.start()
cr_func.readline('press return to close')
import data_io
import strategies

io = data_io.manager('console', 'console')
ai = strategies.get_strategy('basic')
print('IO: {}; AI: {}'.format(io, ai))
input('press return to close')
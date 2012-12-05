import data_io
import strategies

io = data_io.manager('console', 'console')
ai = strategies.get_strategy('basic')
print('IO: {}; AI: {}'.format(io, ai))

# io.initialize_game()
input('press return to start game:')
io.start()
input('press return to close')
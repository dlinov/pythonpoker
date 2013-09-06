import data_io

print('Python 3.* version. No support for 2.* branch')
io = data_io.Manager('gui', 'gui', 'basic')
print('IO: {}'.format(io))

input('press return to start game:')

io.start()
input('press return to close')

import codec
import tktree
from os import listdir
from os.path import isfile, join

files = [f for f in listdir('tests/') if isfile(join('tests/', f))]

for file in files:
    print(file)
    io = codec.codec()
    io.load('tests/' + file)
    tktree.show(io.t, 'tests/' + file)

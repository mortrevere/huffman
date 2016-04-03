import codec
import tktree
from os import listdir
from os.path import isfile, join

files = [f for f in listdir('tests/') if isfile(join('tests/', f))]

for file in files:
    print(file)
    io = codec.codec()
    io.load('tests/' + file)
    name = file.split("\.")[0]
    tktree.saveasimage("tests/" + name + ".ps", io.t)
    print("Loaded in : {}ms".format(io.stats['loadingTime'] * 1000))

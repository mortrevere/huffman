#!/usr/bin/python3.4

from codec import *

io = codec()
io.load("bf.txt")
indexes = io.t.getIndex()

io.encode()
print(io.decode())

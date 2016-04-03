#!/usr/bin/python3.4

from codec import *

io = codec()
io.load("bf.txt")

source = io.buf
io.encode()

print("Filesize is down by", (io.stats['sourceLen']/io.stats['outLen'])*100, "%")

io.decode()

out = io.buf

print('Self-test result : ', end = '')
if source == out:
    print('ok')
else:
    print('fail')

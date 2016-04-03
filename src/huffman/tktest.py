from codec import *
import tktree

c = codec()
c.load("tests/gadsby.txt")
tktree.show(c.t, 900, 800)

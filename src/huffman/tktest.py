import tktree
from leaf import leaf
from tree import tree

win = tktree.tktree()
t = tree()
dick = {}

with open("tests/short.txt") as f:
    for line in f:
        for c in line.strip():
            dick[ord(c)] = dick.get(ord(c), 0) + 1

for c in dick.keys():
    t.addChild(leaf(c, dick[c]))

win.show(t)
t.dynorg(win, 500, t)
win.show(t)

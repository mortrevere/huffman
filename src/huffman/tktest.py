import tktree
try:
    from .leaf import leaf
    from .tree import tree
except SystemError:
    from leaf import leaf
    from tree import tree


win = tktree.tktree(double=True)
t = tree()
dick = {}

with open("tests/short.txt") as f:
    for line in f:
        for c in line.strip():
            dick[ord(c)] = dick.get(ord(c), 0) + 1

for c in dick.keys():
    t.addChild(leaf(c, dick[c]))

#win.show(t)
#t.dynorg(win, 1000, t)
t.organize()
win.show(t)

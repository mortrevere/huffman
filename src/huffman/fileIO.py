from tree import *
from leaf import *


def readFile1(file):
    t = tree()
    dick = {}

    with open(file) as f:
        for line in f:
            for c in line:
                dick[c] = dick.get(c, 0) + 1

    for c in dick.keys():
        t.addChild(leaf(c, dick[c]))

    t.organize()

    return t

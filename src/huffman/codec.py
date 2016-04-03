from tree import *
from leaf import *

class codec:
"""
        Encoder/decoder for huffman compression
"""

    def __init__(self, path):
        self.t = tree()
        self.dic = {}

        with open(path) as f:
            for line in f:
                for c in line:
                    self.dic[c] = self.dic.get(c, 0) + 1

        for c in self.dic.keys():
            self.t.addChild(leaf(c, self.dic[c]))

        self.t.organize()

    def encode(self):
        pass

    def write():
        pass

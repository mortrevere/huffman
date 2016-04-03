from tree import *
from leaf import *

class codec:
    """
    Encoder/decoder for huffman compression
    """

    def __init__(self):
        self.t = tree()
        self.dic = {}
        self.buf = ''
        self.stats = {'sourceLen' : 0, 'outLen' : 0}

    def load(self, path):
        with open(path) as f:
            for line in f:
                for c in line:
                    self.dic[c] = self.dic.get(c, 0) + 1
                self.buf += line

        for c in self.dic.keys():
            self.t.addChild(leaf(c, self.dic[c]))

        self.stats['sourceLen'] = len(self.buf)
        self.t.organize()

    def encode(self):
        """
        Handle compression
        """
        addr = self.t.getIndex()
        self.buf = ''.join([addr[c] for c in self.buf]) #convert chars to binary strings
        self.buf = [self.buf[i:i+8] for i in range(0, len(self.buf), 8)] #split buffer into bytes (as strings)
        self.buf[-1] += '0' * (8-len(self.buf[-1])) #pad last bits to be exactky a byte
        self.buf = [chr(int(c,2)) for c in self.buf] #bytes to char
        self.buf = ''.join(self.buf) #buf to string

        self.stats['outLen'] = len(self.buf)
        return self.buf

    def decode(self):
        out = ''
        tmp = ['',1]
        self.buf = list(self.buf)
        self.buf = ''.join(['{0:08b}'.format(ord(c)) for c in self.buf])
        while tmp[1] != 0:
            tmp = self.t.getValue(self.buf)
            out += tmp[0]
            self.buf = self.buf[tmp[1]:]
        self.buf = out[0:-1]

        self.stats['outLen'] = len(self.buf)
        return self.buf

    def write(self, path):
        with open(path, 'w') as f:
            f.write(self.buf)

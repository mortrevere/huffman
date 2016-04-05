try:
    from .leaf import leaf
    from .tree import tree

except SystemError:
    from leaf import leaf
    from tree import tree

import time

def rightPad(string):
    while len(string)%8 != 0:
        string += '0'
    return string

class codec:
    """
    Encoder/decoder for huffman compression
    """

    def __init__(self):
        self.t = tree()
        self.dic = {}
        self.buf = []
        self.header = []
        self.isCompressed = False
        self.stats = {
            'sourceLen': 0, 'outLen': 0, 'processTime': 0, 'loadingTime': 0, 'compressionRate' : 0}

    def load(self, path, debug = 0):
        t1 = time.clock()
        self.treeLen = 0
        self.bodyLen = 0

        with open(path, "rb") as f:
            seek = 0

            byte = f.read(4096)
            while byte:
                for c in byte:
                    #we build the header even if we are loading an uncompressed file
                    if seek <= 1: #bytes coding tree length if compressed file
                        self.treeLen += c * (-255*seek + 256)
                    if 2 <= seek <= self.treeLen + 5:
                        self.header.append(c)

                    self.dic[c] = self.dic.get(c, 0) + 1
                    seek += 1

                self.buf += list(byte)
                byte = f.read(4096)

            self.header = ''.join(['{0:08b}'.format(c) for c in self.header])[0:self.treeLen+24]
            if len(self.header) > 24:
                self.bodyLen = int(self.header[-24:], 2)
                self.header = self.header[0:-24]

        self.stats['sourceLen'] = len(self.buf)
        self.stats['loadingTime'] = time.clock() - t1

    def encode(self):
        """
        Handle compression
        """

        t1 = time.clock()

        for c in self.dic.keys():
            self.t.addChild(leaf(c, self.dic[c]))
        self.t.organize()

        '''
        TODO : size estimation
        lens = {k : len(self.dic[k]) for k in self.t}
        outLen = 0
        '''
        addr = self.t.getIndex()

        self.buf = rightPad(''.join([addr[c] for c in self.buf]))
        self.buf = [self.buf[i:i + 8] for i in range(0, len(self.buf), 8)]
        self.buf = [int(c, 2) for c in self.buf]  # bytes to char

        self.stats['outLen'] = len(self.buf)
        self.stats['processTime'] = round(time.clock() - t1, 6)
        self.isCompressed = True

        return self.buf

    def decode(self):
        t1 = time.clock()

        out = []
        self.t = tree(self.header)
        longestPath = len(self.t)
        rI = self.t.getReverseIndex()

        self.buf = ''.join(['{0:08b}'.format(c) for c in self.buf])
        self.buf = self.buf[len(self.header)+16+24:]

        while self.bodyLen > 0:
            for k in range(1,longestPath):
                tmp = self.buf[0:k]
                if tmp in rI: #lookup in dict is O(1) ! #2fast4u
                    out.append(rI[tmp])
                    self.buf = self.buf[k:]
                    break
            self.bodyLen -= 1

        self.buf = out

        self.stats['outLen'] = len(self.buf)
        self.stats['processTime'] = round(time.clock() - t1, 6)

        return self.buf

    def write(self, path):
        t1 = time.clock()
        if self.isCompressed:
            tree = str(self.t)
            header = tree
            header = '0'*(18-len(bin(len(header)))) + bin(len(header))[2:]
            header += tree
            header += '0'*(26-len(bin(self.stats['sourceLen']))) + bin(self.stats['sourceLen'])[2:]

            self.buf = rightPad(header + ''.join(['{0:08b}'.format(c) for c in self.buf]))
            self.buf = [int(self.buf[i:i + 8],2) for i in range(0, len(self.buf), 8)]

        with open(path, 'wb') as f:
            f.write(bytes(self.buf))

        self.stats['processTime'] = round(time.clock() - t1, 6)
        self.stats['compressionRate'] = round((1 - len(self.buf)/self.stats['sourceLen'])*100,2)


    def close(self):
        self.t = tree()
        self.dic = {}
        self.buf = []
        self.header = []
        self.bodyLen = 0
        self.treeLen = 0
        self.isCompressed = False

        self.stats = {
            'sourceLen': 0, 'outLen': 0, 'processTime': 0, 'loadingTime': 0, 'compressionRate' : 0}

try:
    from .leaf import leaf
    from .tree import tree
    from .entro import learnEntropy
except SystemError:
    from leaf import leaf
    from tree import tree
    from entro import learnEntropy

import time
import os
from math import log2
from collections import deque

def rightPad(string):
    while len(string)%8 != 0:
        string += '0'
    return string

class progress:

    def __init__(self, var):
        self.var = var
        self.max = 0
        self.current = 0

    def tick(self):
        self.current += 1;
        #trying to avoid perf issues by updating tkVars at too HF
        tmp = round(self.current*100/self.max)
        if self.var == None:
            return 0;
        if tmp != self.var.get():
            self.var.set(tmp)

    def jump(self, n):
        if self.var == None:
            return 0;
        self.current += n;
        self.var.set(round(self.current*100/self.max))

    def reset(self):
        self.max = 0
        self.current = 0

class codec:
    """
    Encoder/decoder for huffman compression
    """

    def __init__(self, progressVar = None):
        self.t = tree()
        self.dic = {}
        self.buf = []
        self.header = []
        self.isCompressed = False
        self.progress = progress(progressVar)
        self.stats = {
            'sourceLen': 0, 'outLen': 0, 'processTime': 0,'preOutLen' : 0,'typeEntropy' : 0, 'compressionRate' : 0}

    def load(self, path, debug = 0):
        """
        Handle input from disk and header parsing
        path is a string containing the path of the file to compress/decompress
        """

        t1 = time.clock()
        self.treeLen = 0
        self.bodyLen = 0

        self.progress.max = os.path.getsize(path)

        with open(path, "rb") as f:
            seek = 0

            byte = f.read(2048)
            while byte:
                for c in byte:
                    #we build the header even if we are loading an uncompressed file
                    if seek <= 1: #bytes coding tree length if compressed file
                        self.treeLen += c * (-255*seek + 256)
                    if 2 <= seek <= self.treeLen + 5:
                        self.header.append(c)

                    self.dic[c] = self.dic.get(c, 0) + 1
                    seek += 1
                    self.progress.tick()

                self.buf += list(byte)
                byte = f.read(4096)

            self.header = ''.join(['{0:08b}'.format(c) for c in self.header])[0:self.treeLen+24]
            if len(self.header) > 24:
                self.bodyLen = int(self.header[-24:], 2)
                self.header = self.header[0:-24]

        self.stats['processTime'] = time.clock() - t1
        self.stats['sourceLen'] = len(self.buf)

        ext = path.split(".")[-1]
        if ext != "clh":
            p = [self.dic[k]/self.stats['sourceLen'] for k in self.dic.keys()]
            self.stats['typeEntropy'] = - sum([pi*log2(pi) for pi in p])
            learnEntropy(ext, self.stats['typeEntropy'])
            self.stats['preOutLen'] = (self.stats['typeEntropy']+min(self.stats['typeEntropy']+1,8))*self.stats['sourceLen']/16

        self.progress.reset()

    def encode(self):
        """
        Handle compression
        """

        t1 = time.clock()

        self.progress.max = len(self.dic.keys())

        for c in self.dic.keys():
            self.t.addChild(leaf(c, self.dic[c]))
            self.progress.tick()
        self.t.organize()

        self.progress.reset()

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
        shortestPath = len(min(rI.keys(), key = len))

        self.buf = ''.join(['{0:08b}'.format(c) for c in self.buf])
        self.buf = self.buf[len(self.header)+16+24:]
        self.progress.max = self.bodyLen

        self.buf = deque(self.buf) #using deque instead of lists brings perfs to life, approaching linear time O(n)
        while self.bodyLen > 0:
            tmp = ''
            while tmp not in rI:
                tmp += self.buf.popleft()
                if tmp in rI: #lookup in dict is O(1) ! #2fast4u
                    out.append(rI[tmp])
                    break
            self.bodyLen -= 1
            self.progress.tick()

        """
        Old way of decoding : probably O(n²) due to string cutting ... quite bad
        Kept here for comparison purpose
        while self.bodyLen > 0:
            for k in range(shortestPath,longestPath):
                tmp = self.buf[0:k]
                if tmp in rI: #lookup in dict is O(1) ! #2fast4u
                    out.append(rI[tmp])
                    self.buf = self.buf[k:]
                    break
            self.bodyLen -= 1
            self.progress.tick()
        """

        self.buf = out
        self.progress.reset()

        self.stats['outLen'] = len(self.buf)
        self.stats['processTime'] = round(time.clock() - t1, 6)

        return self.buf

    def write(self, path):
        """
        Handle output to disk
        path is a string containing the path to the output file
        """
        t1 = time.clock()
        self.progress.max = len(self.buf)

        if self.isCompressed:
            self.progress.max *= 3
            tree = str(self.t)
            header = tree
            header = '0'*(18-len(bin(len(header)))) + bin(len(header))[2:]
            header += tree
            header += '0'*(26-len(bin(self.stats['sourceLen']))) + bin(self.stats['sourceLen'])[2:]
            self.buf = rightPad(header + ''.join(['{0:08b}'.format(c) for c in self.buf]))
            self.progress.jump(self.progress.max*1/3)
            self.buf = [int(self.buf[i:i + 8],2) for i in range(0, len(self.buf), 8)]
            self.progress.jump(self.progress.max*1/3)

        with open(path, 'wb') as f:
            f.write(bytes(self.buf))

        self.progress.current = self.progress.max - 1
        self.progress.tick()
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
            'sourceLen': 0, 'outLen': 0, 'processTime': 0,'preOutLen' : 0,'typeEntropy' : 0, 'compressionRate' : 0}

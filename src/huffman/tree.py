import leaf


class tree:
    """
    The huffman tree itself.
    Each node child of each node can be another tree or a leaf.
    """

    def __init__(self, arg1=[]):
        self.parent = None
        self.isLeaf = False
        if isinstance(arg1, str):
            p = arg1[4:]
            n1 = int(arg1[:4], 2)
            k = 0
            dic = {}  # We recreate the reverse index from addresses
            while k < 256:
                n2 = int(p[:n1], 2)  # nb of bits to code the add
                dic[p[n1:n1 + n2]] = chr(k)  # reverse index
                p = p[n1 + n2:]
                k += 1
            arg1 = dic
        if isinstance(arg1, dict):
            if arg1.get("0", None) is not None:
                self.addChild(leaf.leaf(arg1["0"]))
            else:
                self.addChild(
                    tree({k[1:]: arg1[k] for k in arg1.keys() if k[0] == "0"}))
            if arg1.get("1", None) is not None:
                self.addChild(leaf.leaf(arg1["1"]))
            else:
                self.addChild(
                    tree({k[1:]: arg1[k] for k in arg1.keys() if k[0] == "1"}))
        else:
            self.setChildren(arg1)
            self.setW()
        

    def disp(self, lvl=0):
        print("--" * lvl + "(" + str(self.w) + ")")
        for child in self.children:
            child.disp(lvl + 1)

    def addChild(self, child):
        child.parent = self
        self.children.append(child)
        self.setW()
        if self.parent is not None:
            self.parent.setW()

    def addChildren(self, children):
        for child in children:
            self.addChild(child)

    def setChildren(self, children):
        self.children = []
        self.addChildren(children)

    def setW(self):
        self.w = 0
        for child in self.children:
            self.w += child.w

    def sort(self):
        self.children = sorted(self.children, key=lambda a: a.w)

    def organize(self):
        while len(self.children) > 2:
            self.sort()
            self.setChildren(
                [tree([self.children[0], self.children[1]])] +
                self.children[2:])
        for child in self.children:
            child.organize()

    def getIndex(self):
        d0 = self.children[0].getIndex()
        for k in d0.keys():
            d0[k] = "0" + d0[k]

        d1 = self.children[1].getIndex()
        for k in d1.keys():
            d1[k] = "1" + d1[k]

        d0.update(d1)

        return d0

    def getValue(self, address, length=0):
        if address != '':
            return self.children[int(str(address[0]))].getValue(address[1:],
                                                                length + 1)
        else:
            return ('', 0)

    def __len__(self):
        return max([1 + len(child) for child in self.children])

    def getSize(self):
        return sum([child.getSize() for child in self.children])

    def __repr__(self):
        return str(self.w)

    def __str__(self):
        dic = self.getIndex()
        # number of bits to code the max depth
        m = len(bin(len(self))) - 2
        s = '{0:04b}'.format(m)
        for k in range(256):
            add = dic.get(ord(k), "")
            s += ('{0:0' + m + 'b}{}').format(len(add), add)
        return s

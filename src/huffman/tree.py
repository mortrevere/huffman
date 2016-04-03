class tree:
    """
    The huffman tree itself.
    Each node child of each node can be another tree or a leaf.
    """

    def __init__(self, arg1=[]):
        if isinstance(arg1, str):
            # delete first [ and last ] then split with ] and delete last
            # element that is empty
            p = arg1[1:-1].split("]")[:-1]
            self.setChildren([e+"]" for e in p])
        else:
            self.setChildren(arg1)
        self.parent = None
        self.setW()
        self.isLeaf = False

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
        s = "["
        for child in self.children:
            s += str(child)
        return s + "]"

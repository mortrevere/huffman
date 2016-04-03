class tree:
    """
    The huffman tree itself.
    Each node child of each node can be another tree or a leaf.
    """

    def __init__(self, children=[]):
        self.parent = None
        self.setChildren(children)
        self.w = 0
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

    def __str__(self):
        return str(self.w)

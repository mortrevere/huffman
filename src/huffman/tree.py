try:
    from . import leaf
except SystemError:
    import leaf


def getReverseIndex(arg1):
    """
    Transform binary data of the tree into a reversed index path->letter
    """
    p = arg1[4:]
    n1 = int(arg1[:4], 2)
    k = 0
    dic = {}  # We recreate the reverse index from addresses
    while k < 256:
        n2 = int(p[:n1], 2)  # nb of bits to code the add
        add = p[n1:n1 + n2]
        if add != "":
            dic[p[n1:n1 + n2]] = k  # reverse index
        p = p[n1 + n2:]
        k += 1
    return dic


def getASCIIIndex():
    """
    Return the tree from the ascii table (binary paths)
    """
    dic = {}
    for k in range(256):
        dic[chr(k)] = "{:0>8}".format(bin(k)[2:])
    return dic


def getRootTree(text):
    dic = {}
    for c in text:
        dic[c] = dic.get(c, 0) + 1
    print(dic)
    t = tree()
    for c in dic.keys():
        t.addChild(leaf.leaf(ord(c), dic[c]))
    return t


class tree:
    """
    The huffman tree itself.
    Each node child of each node can be another tree or a leaf.
    """

    def __init__(self, arg1=[]):
        self.parent = None
        self.children = []
        if isinstance(arg1, str):
            arg1 = getReverseIndex(arg1)
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
        """
        Display the tree for debug purposes
        """
        print("--" * lvl + "(" + str(self.w) + ")")
        for child in self.children:
            child.disp(lvl + 1)

    def addChild(self, child):
        """
        Add the given child in the node
        """
        child.parent = self
        self.children.append(child)
        self.setW()
        if self.parent is not None:
            self.parent.setW()

    def addChildren(self, children):
        """
        Add multiple children in the node
        """
        for child in children:
            self.addChild(child)

    def setChildren(self, children):
        """
        Replace all the children
        """
        self.children = []
        self.addChildren(children)

    def setW(self):
        """
        Update the weight of the node
        """
        self.w = 0
        for child in self.children:
            self.w += child.w

    def sort(self):
        """
        Sort children with their weight
        """
        self.children = sorted(self.children, key=lambda a: a.w)

    def organize(self):
        """
        Make the final tree from all leaves into the root
        """
        while len(self.children) > 2:
            self.sort()
            self.setChildren(
                [tree([self.children[0], self.children[1]])] +
                self.children[2:])

    def dynorg(self, win, time, root):
        """
        Same as organize() but with graphic visualization
        """
        win.show(root, time)
        while len(self.children) > 2:
            self.sort()
            self.setChildren(
                [tree([self.children[0], self.children[1]])] +
                self.children[2:])
            win.show(root, time)
            self.sort()
            win.show(root, time)

    def getIndex(self):
        """
        Return the index of the tree (letter->path)
        """
        d0 = self.children[0].getIndex()
        for k in d0.keys():
            d0[k] = "0" + d0[k]
        d1 = self.children[1].getIndex()
        for k in d1.keys():
            d1[k] = "1" + d1[k]
        d0.update(d1)
        return d0

    def getReverseIndex(self):
        """
        Return the revers-index of the tree (path->letter)
        """
        ind = self.getIndex()
        return {ind[k]: k for k in ind.keys()}

    def getValue(self, path, k=0, length=0):
        """
        Return the value with the given path
        """
        if path != '':
            return self.children[int(str(path[k]))].getValue(path,
                                                                k + 1,
                                                                length + 1)
        else:
            return ('', 0)

    def __len__(self):
        """
        Return the max depht of the tree
        """
        return max([1 + len(child) for child in self.children])

    def getSize(self):
        """
        Return the max number of children in all depths
        """
        return sum([child.getSize() for child in self.children])

    def __str__(self):
        """
        Transform the tree into a binary string for compression
        """
        dic = self.getIndex()
        # number of bits to code the max depth
        m = len(bin(len(self))) - 2
        s = '{0:04b}'.format(m)
        for k in range(256):
            add = dic.get(k, "")
            s += ('{0:0' + str(m) + 'b}').format(len(add)) + add
        return s
    
    def __repr__(self):
        return str(self.w)

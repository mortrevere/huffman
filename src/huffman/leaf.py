class leaf:
    """
    Leaves of a huffman tree
    """

    def __init__(self, arg1, w=0):
        if isinstance(arg1, str):
            self.value = arg1[1:-1]
        else:
            self.value = arg1
        self.w = w
        self.parent = None
        self.isLeaf = True

    def disp(self, lvl=0):
        print("--" * lvl + "({}, {})".format(self.value, self.w))

    def organize(self):
        return True

    def getIndex(self):
        return {self.value: ""}

    def getValue(self, address, length):
        return (self.value, length)

    def __len__(self):
        return 1

    def getSize(self):
        return 1

    def __repr__(self):
        return str(self.value)+":"+str(self.w)

    def __str__(self):
        return "["+str(self.value)+"]"

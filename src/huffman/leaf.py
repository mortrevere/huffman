class leaf:
    """
    Leaves of a huffman tree
    """

    def __init__(self, value, w):
        self.parent = None
        self.value = value
        self.w = w
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

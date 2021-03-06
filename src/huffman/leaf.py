class leaf:
    """
    Leaves of a huffman tree
    """

    def __init__(self, value, w=0):
        self.value = value
        self.w = w
        self.parent = None

    def disp(self, lvl=0):
        print("--" * lvl + "({}, {})".format(self.value, self.w))

    def organize(self):
        return True

    def getIndex(self):
        return {self.value: ""}

    def getValue(self, path, k, length):
        return (self.value, length)

    def __len__(self):
        return 1

    def getSize(self):
        return 1

    def __repr__(self):
        return str(chr(self.value))+":"+str(self.w)

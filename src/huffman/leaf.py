class leaf:
    """
    Leaves of a huffman tree
    """

    def __init__(self, value, w):
        self.parent = None
        self.value = value
        self.w = w

    def print(self, lvl=0):
        print("--" * lvl + "({}, {})".format(self.value, self.w))

    def organize(self):
        return True

    def getIndex(self):
        return {self.value: ""}

    def getValue(self, address):
        return self.value

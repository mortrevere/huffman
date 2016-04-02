class leaf:

    def __init__(self, value, w):
        self.parent = None
        self.value = value
        self.w = w

    def printt(self, lvl=0):
        print("--" * lvl + "({}, {})".format(self.value, self.w))

    def organize(self):
        return True

    def getIndex(self):
        return {self.value: ""}

class tree:

    def __init__(self, children=[]):
        self.parent = None
        self.setChildren(children)
        self.w = 0
        self.setW()

    def printt(self, lvl=0):
        print("--" * lvl + "(" + str(self.w) + ")")
        for child in self.children:
            child.printt(lvl + 1)

    def addChild(self, child):
        child.parent = self
        self.children.append(child)
        self.setW()
        if self.parent != None:
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
            # Il faut jamais modifier le self.children directement
            self.setChildren(
                [tree([self.children[0], self.children[1]])] + self.children[2:])
        for child in self.children:
            child.organize()

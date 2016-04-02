class tree:
    def __init__(self, children = []):
        self.parent = None
        self.children = children.copy()
        self.w = 0
        self.setW()
    
    def print(self, lvl = 0):
        print("--" * lvl + "(" + str(self.w) + ")")
        for child in self.children:
            child.print(lvl + 1)

    def addChild(self, child):
        child.parent = self
        self.children.append(child)
        self.setW()
        if self.parent != None:
            self.parent.setW()
        
    def addChildren(self, children):
        for child in children:
            self.addChild(child)

    def setW(self):
        self.w = 0
        for child in self.children:
            self.w += child.w 
    def sort(self):
        self.children = sorted(self.children, key=lambda a: a.w)

class leaf:
    def __init__(self, value, w):
        self.parent = None
        self.value = value
        self.w = w
    def print(self, lvl = 0):
        print("--" * lvl + "({}, {})".format(self.value, self.w))
    
    

'''t = tree()
for i in range(10):
    t.addChild(leaf(i,i))

eval("t")'''

t = tree()
dick = {}

with open("mathinfo.py") as f:
    for line in f:
        for c in line.strip():
            dick[c] = dick.get(c,0) + 1

for c in dick.keys():
    t.addChild(leaf(c,dick[c]))

t.print()
t.sort()
t.print()

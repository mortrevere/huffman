# Huffman Tree
## I - Theory
### A - Definition
A huffman tree is composed of nodes and leaves. Each possesses a weight that help sorting them. The heavier a node or a leaf is, the closer to the root it is. If the leaf weight represent a letter frequency, it means that a frequent letter have a short path in the tree and getting to it cost less data.

![alt text][example1]

Here we create a tree from the sentence "this is a short example".
We can see each node with its weight and each leaf (higlighted) with the letter it represent and its weight/number of occurences.
### B - Basic technique of creation
We start from a text, (in every example, we're going to use "this is a short example" for the simplicity) and we create at the root each leaves. Each leaves is created from a letter and its number of occurences. Then we can start organizing the tree. First we take the two lighter nodes/leaves of the root and we group them in a single node. We repeat this traitment until there is only two nodes/leaves left

![alt text][example2]

Here we can see this technique in action on our example. 
### C - Compression/Decompression
### D - Canonical Huffman
## II - Python Implementation
### A - Building
#### __init__
```python
	def __init__(self, arg1=[]):
	        self.parent = None
	        self.isLeaf = False
	        self.setChildren(arg1)
	        self.setW()
```
#### addChild/addChildren/setChildren
```python
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
```
#### setW
```python
	def setW(self):
        self.w = 0
        for child in self.children:
            self.w += child.w
```
#### sort
```python
	def sort(self):
        self.children = sorted(self.children, key=lambda a: a.w)
```
#### organize
```python
	def organize(self):
        while len(self.children) > 2:
            self.sort()
            self.setChildren(
                [tree([self.children[0], self.children[1]])] +
                self.children[2:])
        for child in self.children:
            child.organize()
```
### B - Visualization
#### Console
```python
	def disp(self, lvl=0):
        print("--" * lvl + "(" + str(self.w) + ")")
        for child in self.children:
            child.disp(lvl + 1)
```
#### Tkinter
```python
	def __len__(self):
        return max([1 + len(child) for child in self.children])
	
	def getSize(self):
        return sum([child.getSize() for child in self.children])
```
### C - Compression functions
#### Index
```python
	def getIndex(self):
        d0 = self.children[0].getIndex()
        for k in d0.keys():
            d0[k] = "0" + d0[k]

        d1 = self.children[1].getIndex()
        for k in d1.keys():
            d1[k] = "1" + d1[k]

        d0.update(d1)

        return d0
```
#### getValue
```python
	def getValue(self, address, length=0):
        if address != '':
            return self.children[int(str(address[0]))].getValue(address[1:],
                                                                length + 1)
        else:
            return ('', 0)
```
#### Parsing and str builder
```python
	def __str__(self):
        dic = self.getIndex()
        # number of bits to code the max depth
        m = len(bin(len(self))) - 2
        s = '{0:04b}'.format(m)
        for k in range(256):
            add = dic.get(k, "")
            s += ('{0:0' + str(m) + 'b}').format(len(add)) + add
        return s
```
```python
	def __init__(self, arg1=[]):
        self.parent = None
        self.isLeaf = False
        self.children = []
        if isinstance(arg1, str):
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
            arg1 = dic
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
```

[example1]: https://github.com/mortrevere/huffman/raw/master/doc/img/exampletree.png "An example with 'this is a short example'"
[example2]: https://github.com/mortrevere/huffman/raw/master/doc/img/exampletree.gif "An example of tree creation"

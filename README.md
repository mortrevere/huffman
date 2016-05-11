# Huffman
## Table of contents
### [I - Utilization](#i---utilization)
### [II - Theory](#ii---theory)
## I - Utilization
### A - Installation
Download the source folder from github [here](https://github.com/mortrevere/huffman/archive/master.zip). Decompress the archive into desired location and add the src/huffman folder in your Python path. (See how on windows [here](https://docs.python.org/3/using/windows.html#excursus-setting-environment-variables))
### B - Module command
You can now use the huffman compression with the following syntax in a command prompt :

    python -m huffman [source] [destination]

## II - Theory
### A - Huffman Tree
#### 1 - Definition
A tree is a data-structure composed of nodes and leaves. Each leaf is a data and there is a node path to access it. In an Huffman tree, each leaf and node possesses a weight that help organizing the tree. The heavier a node or a leaf is, the closer to the root it is. If the leaf weight represent a letter frequency, it means that a frequent letter have a short path in the tree and getting to it cost less data.

![alt text][example1]

Here we create a tree from the sentence "this is a short example".
We can see each node with its weight and each leaf (highlighted) with the letter it represent and its weight/number of occurrences. Each node possesses only two children to create a binary path for future [compression](#c---compressiondecompression).
#### 2 - Basic technique of creation
We start from a text, (in every example, we're going to use "this is a short example" for the simplicity) and we create at the root each leaves. Each leaves is created from a letter and its number of occurrences. Then we can start organizing the tree. First we take the two lighter nodes/leaves of the root and we group them in a single node. We repeat this treatment until there is only two nodes/leaves left

![alt text][example2]

Here we can see this technique in action on our example. 
#### 3 - Compression/Decompression
The generated tree can be resumed into an index : each letter as a equivalent binary path.

Letter | Path
:---: | :---:
s | 000
i | 0010
t | 0011
r | 01000
x | 01001
... | ...

As we can see here, the binary path is less than an octet witch means that if we replace the actual character with its binary path, the file contains less bits. 
In the generated file, we can't read anything without knowing the index, that's why the decompression need the tree or the index to do so. Technically speaking the decompression isn't hard as we just have to do the reverse as compression but the main problem is in the tree. There is several methods to get the tree for decompressing :

* Static :
The tree is fixed and generated with probability over a large amount of data of a fixed type. It cost no additional bits but the compression can't be done on any type of data.
* Semi-adaptable :
The tree is generated before the compression by reading the file. It's transferred to the decompression by becoming the header of the file. This can be done on any type of data but it cost several additional bits to transfer the tree.
* Adaptable :
The tree is known but dynamically modified during the compression. In the decompression the same modifications are done from the same tree so at the same instant the two trees are equals and the translation is correct. The modification of a tree is done by incrementing the occurrence of a letter and updating its leaf position. The compression is minimal at the beginning but become great over time. The main advantage is there is no initialization and no tree to transfer but the real-time modification of the tree takes a lot of resources.
For this project we will use the semi-adaptable method.

#### 4 - Canonical Huffman
The semi-adaptable method rises issues about the format of the tree when it comes to transferring it. We can regenerate the tree from the index every-time so transferring the index is the main goal here. So the index is like several tuple : the letter and path :
```
(a,111) (e,100) (h,101) (i,0010) ...
```
Keep in mind that for a bigger text, we can imagine every letters represented.
There is another data on this index, the length of the path :
```
(a,3,111) (e,3,100) (h,3,101) (i,4,0010) ...
```
The length of the path is exactly what allows compression.
We will make the letter information implicit by creating a tuple for every letter :
```
(a,3,111) (b,0) (c,0) (d,0) (e,3,100) ...
```
So now there is no need to represent letters as we know the order of them :
```
(3,111) (0) (0) (0) (3,100) ...
```
That's the information we will transfer alongside the file to decompress it.


[example1]: https://github.com/mortrevere/huffman/raw/master/doc/img/exampletree.png "An example with 'this is a short example'"
[example2]: https://github.com/mortrevere/huffman/raw/master/doc/img/exampletree.gif "An example of tree creation"


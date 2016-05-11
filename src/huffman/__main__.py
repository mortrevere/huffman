import sys
from huffman.entro import getEntropy
try:
    from . import codec
    from .window import window, getSize
    from .entro import getEntropy
except SystemError:
    import codec
    from window import window, getSize
    from entro import getEntropy
import os


def win():
    window()


def compress(src, dest):
    print("Compressing " + src + " to " + dest + " ...")
    ext = src.split(".")[-1]
    ent = getEntropy(ext)
    if ent != 0:
        pre = os.path.getsize(src) * (ent + min(ent + 1, 8)) / 16
        print("Estimated output file size : " + getSize(pre))
    c = codec.codec()
    print("Loading source file...")
    c.load(src)
    print("Source file loaded in {} ms".format(
        round(c.stats['processTime'] * 1000, 2)))
    print("Encoding source file...")
    c.encode()
    print("Source file encoded in {} ms".format(
        round(c.stats['processTime'] * 1000, 2)))
    print("Writing destination file...")
    c.write(dest)
    print("Destination file written in {} ms".format(
        round(c.stats['processTime'] * 1000, 2)))
    print("Compression successful !")


def decompress(src, dest):
    print("Uncompressing " + src + " to " + dest + " ...")
    c = codec.codec()
    print("Loading source file...")
    c.load(src)
    print("Source file loaded in {} ms".format(
        round(c.stats['processTime'] * 1000, 2)))
    print("Decoding source file...")
    c.encode()
    print("Source file decoded in {} ms".format(
        round(c.stats['processTime'] * 1000, 2)))
    print("Writing destination file...")
    c.write(dest)
    print("Destination file written in {} ms".format(
        round(c.stats['processTime'] * 1000, 2)))
    print("Uncompression successful !")

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        win()
    elif len(args) == 3:
        c1 = args[1].split(".")[-1] == "clh" or args[1].split(".")[-1] == "clz"
        c2 = args[2].split(".")[-1] == "clh" or args[2].split(".")[-1] == "clz"
        if not c1 and not c2:
            print(
                "The source or the destination file should be .clh or .clz format.")
        elif c1:
            decompress(args[1], args[2])
        else:
            compress(args[1], args[2])
    else:
        print("Please indicate source and destination \
        file or leave blank for the window.")

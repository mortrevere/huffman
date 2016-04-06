import sys
try:
    from . import codec
    from .window import window
except SystemError:
    import codec
    from window import window


def win():
    window()


def compress(src, dest):
    print("Compressing " + src + " to " + dest + " ...")
    c = codec.codec()
    print("Loading source file...")
    c.load(src)
    print("Source file loaded in {.2f} ms".format(
        c.stats['loadingTime'] * 1000))
    print("Encoding source file...")
    c.encode()
    print("Source file encoded in {.2f} ms".format(
        c.stats['processTime'] * 1000))
    print("Writing destination file...")
    c.write(dest)
    print("Destination file written in {.2f} ms".format(
        c.stats['processTime'] * 1000))
    print("Compression successful !")


def decompress(src, dest):
    print("Uncompressing " + src + " to " + dest + " ...")
    c = codec.codec()
    print("Loading source file...")
    c.load(src)
    print("Source file loaded in {.2f} ms".format(
        c.stats['loadingTime'] * 1000))
    print("Decoding source file...")
    c.encode()
    print("Source file decoded in {.2f} ms".format(
        c.stats['processTime'] * 1000))
    print("Writing destination file...")
    c.write(dest)
    print("Destination file written in {.2f} ms".format(
        c.stats['processTime'] * 1000))
    print("Uncompression successful !")

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        win()
    elif len(args) == 3:
        c1 = args[1].split(".")[-1] == "clh"
        c2 = args[2].split(".")[-1] == "clh"
        if not c1 and not c2:
            print("The source or the destination file should be .clh format.")
        elif c1:
            decompress(args[1], args[2])
        else:
            compress(args[1], args[2])
    else:
        print("Please indicate source and destination \
        file or leave blank for the window.")

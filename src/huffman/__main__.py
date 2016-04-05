import sys
try:
    from . import codec
except SystemError:
    import codec
import tkinter as tk
import tkinter.filedialog as tkf
import tkinter.ttk as ttk

FONT = ("Helvetica", 10)
FONTB = ("Helvetica", 10, "bold")
srctypes = [('all files', '.*')]
dsttypes = [('compressed file', '.clh'), ('all files', '.*')]
comp = True


def window():
    global c, win, fr, b1, b2, src, dst
    c = codec.codec()
    win = tk.Tk()
    win.title("Huffman")
    src = tk.StringVar()
    dst = tk.StringVar()
    fr = tk.Frame(win)
    tk.Label(fr, text="Source : ", font=FONT).grid(row=1, column=0,
                                                   sticky=tk.E)
    tk.Entry(fr, textvariable=src, width=30).grid(
        row=1, column=1, columnspan=2)
    tk.Button(fr, text=" ... ", command=lambda: open(
        "Choose source file", src)).grid(row=1, column=3,
                                         sticky=tk.W)
    tk.Label(fr, text="Destination : ", font=FONT, width=10).grid(
        row=2, column=0, sticky=tk.E)
    tk.Entry(fr, textvariable=dst, width=30).grid(
        row=2, column=1, columnspan=2)
    tk.Button(fr, text=" ... ", command=lambda: save(
        "Choose destination file", dst)).grid(row=2, column=3,
                                              sticky=tk.W)
    b1 = tk.Button(fr, text="Compress", width=20, state=tk.DISABLED, bg="lightgrey",
                   command=compressmode)
    b1.grid(row=3, column=0, columnspan=2)
    b2 = tk.Button(fr, text="Uncompress", width=20, command=decompressmode)
    b2.grid(row=3, column=2, columnspan=2)
    tk.Button(fr, text="Launch", font=FONT, width=37, command=process).grid(
        row=4, column=0, columnspan=4)
    fr.pack(padx=5, pady=5)
    win.mainloop()
    # TODO


def compressmode():
    global srctypes, dsttypes, comp
    srctypes, dsttypes = dsttypes, srctypes
    b1.config(state=tk.DISABLED, bg="lightgrey")
    b2.config(state=tk.NORMAL, bg=win.cget("bg"))
    comp = True


def decompressmode():
    global srctypes, dsttypes, comp
    srctypes, dsttypes = dsttypes, srctypes
    b2.config(state=tk.DISABLED, bg="lightgrey")
    b1.config(state=tk.NORMAL, bg=win.cget("bg"))
    comp = False


def process(state=0):
    global l1, p1, l2, p2, l3, p3
    if state == 0:
        p1 = tk.IntVar(0)
        p2 = tk.IntVar(0)
        p3 = tk.IntVar(0)
        l1 = tk.Label(fr, text="Loading : ", font=FONTB)
        l1.grid(row=5, column=0, sticky=tk.E)
        ttk.Progressbar(fr, variable=p1, length=200).grid(
            row=5, column=1, columnspan=2)
        l2 = tk.Label(fr, text="Decoding : ", font=FONT)
        if comp:
            l2.config(text="Encoding : ")
        l2.grid(row=6, column=0, sticky=tk.E)
        ttk.Progressbar(fr, variable=p2, length=200).grid(
            row=6, column=1, columnspan=2)
        l3 = tk.Label(fr, text="Writing : ", font=FONT)
        l3.grid(row=7, column=0, sticky=tk.E)
        ttk.Progressbar(fr, variable=p3, length=200).grid(
            row=7, column=1, columnspan=2)
        c.load(src.get())
    elif state == 1:
        l1.config(font=FONT)
        l2.config(font=FONTB)
        p1.set(100)
        c.encode()
    elif state == 2:
        l2.config(font=FONT)
        l3.config(font=FONTB)
        p2.set(100)
        dest = dst.get()
        if comp and not ".clh" in dest:
            dest += ".clh"
        c.write(dest)
    else:
        l3.config(font=FONT)
        p3.set(100)
        c.close()
        state = -1
    if state != -1:
        win.after(100, lambda: process(state + 1))


def open(title, tkvar):
    tkvar.set(tkf.askopenfilename(
        title=title, initialfile=tkvar.get(), filetypes=srctypes))


def save(title, tkvar):
    tkvar.set(tkf.asksaveasfilename(
        title=title, initialfile=tkvar.get(), filetypes=dsttypes))


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
    c.write(dest, enc=True)
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
    c.write(dest, enc=True)
    print("Destination file written in {.2f} ms".format(
        c.stats['processTime'] * 1000))
    print("Uncompression successful !")

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        window()
    elif len(args) == 3:
        c1 = args[1].split("\.")[-1] == "clh"
        c2 = args[2].split("\.")[-1] == "clh"
        if not c1 and not c2:
            print("The source or the destination file should be .clh format.")
        elif c1:
            decompress(args[1], args[2])
        else:
            compress(args[1], args[2])
    else:
        print("Please indicate source and destination \
        file or leave blank for the window.")

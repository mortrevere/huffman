try:
    from . import codec
    from .tktree import tktree
    from .tree import tree
except SystemError:
    import codec
    from tktree import tktree
    from tree import tree
import tkinter as tk
import tkinter.filedialog as tkf
import tkinter.ttk as ttk

FONT = ("Helvetica", 10)
FONTB = ("Helvetica", 10, "bold")


class window:
    def __init__(self):
        self.c = codec.codec()

        self.win = tk.Tk()
        self.win.title("Huffman")
        self.win.resizable(False, False)
        self.srcv = tk.StringVar()
        self.dstv = tk.StringVar()
        self.src = ""
        self.dst = ""
        self.srctypes = [('all files', '.*')]
        self.dsttypes = [('compressed file', '.clh'), ('all files', '.*')]
        self.comp = True
        self.launch = False
        self.source = ""
        self.state = 0
        self.p1 = tk.IntVar(0)
        self.p2 = tk.IntVar(0)
        self.p3 = tk.IntVar(0)

        self.win1()

        self.win.mainloop()

    def changemode(self):
        self.srctypes, self.dsttypes = self.dsttypes, self.srctypes
        self.comp = not self.comp
        self.srcv.set("")
        self.dstv.set("")
        self.bl.config(state=tk.DISABLED)
        if self.comp:
            self.bm.config(text="Compress")
        else:
            self.bm.config(text="Uncompress")

    def win1(self):
        self.fr = tk.Frame(self.win)

        tk.Label(self.fr, text="Mode : ", font=FONT).grid(row=0, column=0, sticky=tk.E)
        self.bm = tk.Button(self.fr, text="Compress", width=28, command=self.changemode)
        self.bm.grid(row=0, column=1, columnspan=3)

        tk.Label(self.fr, text="Source : ", font=FONT).grid(row=1, column=0, sticky=tk.E)
        tk.Entry(self.fr, textvariable=self.srcv, width=30, state=tk.DISABLED).grid(row=1, column=1, columnspan=2)
        self.bs = tk.Button(self.fr, text=" ... ", command=self.open)
        self.bs.grid(row=1, column=3, sticky=tk.W)

        tk.Label(self.fr, text="Destination : ", font=FONT, width=10).grid(row=2, column=0, sticky=tk.E)
        tk.Entry(self.fr, textvariable=self.dstv, width=30, state=tk.DISABLED).grid(row=2, column=1, columnspan=2)
        self.bd = tk.Button(self.fr, text=" ... ", command=self.save)
        self.bd.grid(row=2, column=3, sticky=tk.W)

        self.bl = tk.Button(self.fr, text="Launch", font=FONT, width=35, state=tk.DISABLED, command=self.process)
        self.bl.grid(row=4, column=0, columnspan=4)

        self.fr.pack(padx=5, pady=5)

    def win2(self):
        self.bs.config(state=tk.DISABLED)
        self.bd.config(state=tk.DISABLED)
        self.bm.config(state=tk.DISABLED)
        self.bl.config(state=tk.DISABLED)
        self.l1 = tk.Label(self.fr, text="Loading : ", font=FONTB)
        self.l1.grid(row=5, column=0, sticky=tk.E)
        ttk.Progressbar(self.fr, variable=self.p1, length=200).grid(row=5, column=1, columnspan=2)
        self.l2 = tk.Label(self.fr, text="Decoding : ", font=FONT)
        if self.comp:
            self.l2.config(text="Encoding : ")
        self.l2.grid(row=6, column=0, sticky=tk.E)
        ttk.Progressbar(self.fr, variable=self.p2, length=200).grid(row=6, column=1, columnspan=2)
        self.l3 = tk.Label(self.fr, text="Writing : ", font=FONT)
        self.l3.grid(row=7, column=0, sticky=tk.E)
        ttk.Progressbar(self.fr, variable=self.p3, length=200).grid(row=7, column=1, columnspan=2)

    def process(self):
        if self.state == 0:
            self.win2()
            self.c.load(self.src)
        elif self.state == 1:
            self.l1.config(font=FONT)
            self.l2.config(font=FONTB)
            self.p1.set(100)
            self.c.encode()
        elif self.state == 2:
            self.l2.config(font=FONT)
            self.l3.config(font=FONTB)
            self.p2.set(100)
            self.c.write(self.dst)
        else:
            self.l3.config(font=FONT)
            self.p3.set(100)
            if self.comp:
                tk.Label(self.fr, text="Compression successful", font=FONTB).grid(row=8, column=0, columnspan=4)
                tk.Label(self.fr, text="Compression rate : {}%".format(self.c.stats['compressionRate']), font=FONT).grid(row=9, column=0, columnspan=2)
                tk.Button(self.fr, text="Show tree", command=self.showtree).grid(row=9, column=2, columnspan=2)
            else:
                tk.Label(self.fr, text="Uncompression successful", font=FONTB).grid(row=8, column=0, columnspan=4)
            self.bl.config(text="New File", command=self.reset, state=tk.NORMAL)
            return True
        self.state += 1
        self.win.after(100, self.process)

    def showtree(self):
        if self.comp:
            t = self.c.t
        else:
            t = tree(self.c.header)
        tktree("clic to quit").show(t)

    def reset(self):
        self.win.destroy()
        self = window()

    def open(self):
        self.src = tkf.askopenfilename(title="Choose source file :", initialfile=self.srcv.get(), filetypes=self.srctypes)
        if self.comp:
            self.dst = self.src+".clh"
        else:
            self.dst = self.src[:-4]
        self.check()

    def save(self):
        self.dst = tkf.asksaveasfilename(title="Choose destination file :", initialfile=self.dstv.get(), filetypes=self.dsttypes)
        self.check()

    def check(self):
        self.srcv.set(self.src.split("/")[-1])
        self.dstv.set(self.dst.split("/")[-1])
        if self.src != "" and self.dst != "":
            self.bl.config(state=tk.NORMAL)
        else:
            self.bl.config(state=tk.DISABLED)

if __name__ == "__main__":
    window()





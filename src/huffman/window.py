try:
    from . import codec
    from .tktree import tktree
    from .tree import tree
    from .entro import getEntropy
except SystemError:
    import codec
    from tktree import tktree
    from tree import tree
    from entro import getEntropy
import tkinter as tk
import tkinter.filedialog as tkf
import tkinter.messagebox as tkm
import tkinter.ttk as ttk
import time
import os

FONT = ("Helvetica", 10)
FONTB = ("Helvetica", 10, "bold")


def getSize(s):
    if s < 10**3:
        return str(round(s,2)) + " o"
    if s < 10**6:
        return str(round(s/10**3, 2)) + " Ko"
    if s < 10**9:
        return str(round(s/10**6, 2)) + " Mo"

class window:

    def __init__(self):

        self.win = tk.Tk()
        self.win.title("Huffman")
        self.win.resizable(False, False)
        self.srcv = tk.StringVar()
        self.dstv = tk.StringVar()
        self.stv = tk.BooleanVar()
        self.stv.set(True)
        self.stv.trace('w', self.stats)
        self.src = ""
        self.dst = ""
        self.srctypes = [('all files', '.*')]
        self.dsttypes = [('compressed file', '.clh'), ('all files', '.*')]
        self.comp = True
        self.launch = False
        self.source = ""
        self.state = 0
        self.prog = tk.IntVar(0)
        self.prog.trace('w', self.refresh)
        self.end = tk.IntVar()
        self.end.set(100)
        self.c = codec.codec(self.prog)
        self.win1()
        self.win.mainloop()

    def refresh(self, *args):
        self.win.update()

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

        tk.Label(self.fr, text="Mode : ", font=FONT).grid(
            row=0, column=0, sticky=tk.E)
        self.bm = tk.Button(
            self.fr, text="Compress", width=28, command=self.changemode)
        self.bm.grid(row=0, column=1, columnspan=3)

        self.srcl = tk.Label(self.fr, text="Source : ", font=FONT)
        self.srcl.grid(row=1, column=0, sticky=tk.E)
        tk.Entry(self.fr, textvariable=self.srcv, width=30, state=tk.DISABLED).grid(
            row=1, column=1, columnspan=2)
        self.bs = tk.Button(self.fr, text=" ... ", command=self.open)
        self.bs.grid(row=1, column=3, sticky=tk.W)

        tk.Label(self.fr, text="Destination : ", font=FONT, width=10).grid(
            row=2, column=0, sticky=tk.E)
        tk.Entry(self.fr, textvariable=self.dstv, width=30, state=tk.DISABLED).grid(
            row=2, column=1, columnspan=2)
        self.bd = tk.Button(self.fr, text=" ... ", command=self.save)
        self.bd.grid(row=2, column=3, sticky=tk.W)
        self.cb = tk.Checkbutton(self.fr, text="show statistics", variable=self.stv)
        self.cb.grid(row=4, column=0, columnspan=2)
        self.bl = tk.Button(self.fr, text="Launch", font=FONT,
                            width=20, state=tk.DISABLED, command=self.process)
        self.bl.grid(row=4, column=2, columnspan=2)

        self.fr.pack(padx=5, pady=5)

    def win2(self):
        self.bs.config(state=tk.DISABLED)
        self.bd.config(state=tk.DISABLED)
        self.bm.config(state=tk.DISABLED)
        self.bl.config(state=tk.DISABLED)
        self.cb.config(state=tk.DISABLED)
        self.l1 = tk.Label(self.fr, text="Loading : ", font=FONTB)
        self.l1.grid(row=5, column=0, sticky=tk.E)
        self.p1 = ttk.Progressbar(self.fr, length=200)
        self.p1.grid(row=5, column=1, columnspan=2)
        self.l2 = tk.Label(self.fr, text="Decoding : ", font=FONT)
        if self.comp:
            self.l2.config(text="Encoding : ")
        self.l2.grid(row=8, column=0, sticky=tk.E)
        self.p2 = ttk.Progressbar(self.fr, length=200)
        self.p2.grid(row=8, column=1, columnspan=2)
        self.l3 = tk.Label(self.fr, text="Writing : ", font=FONT)
        self.l3.grid(row=9, column=0, sticky=tk.E)
        self.p3 = ttk.Progressbar(self.fr, length=200)
        self.p3.grid(row=9, column=1, columnspan=2)

    def process(self):
        if self.state == 0:
            self.win2()
            self.p1.config(variable=self.prog)
        elif self.state == 1:
            self.c.load(self.src)
            self.l1.config(font=FONT)
            self.l2.config(font=FONTB)
            self.p2.config(variable=self.prog)
            self.p1.config(variable=self.end)
            if self.stv.get():
                tk.Label(self.fr, text="{} s".format(round(self.c.stats['processTime'],2)), font=FONT).grid(row=5, column=3)
        elif self.state == 2:
            if self.comp:
                self.c.encode()
            else:
                self.c.decode()
            self.l2.config(font=FONT)
            self.l3.config(font=FONTB)
            self.p3.config(variable=self.prog)
            self.p2.config(variable=self.end)
            if self.stv.get():
                tk.Label(self.fr, text="{} s".format(round(self.c.stats['processTime'],2)), font=FONT).grid(row=8, column=3)
        elif self.state == 3:
            self.c.write(self.dst)
            self.l3.config(font=FONT)
            if self.stv.get():
                tk.Label(self.fr, text="{} s".format(round(self.c.stats['processTime'],2)), font=FONT).grid(row=9, column=3)
        else:
            if self.comp:
                tk.Label(self.fr, text="Compression successful", font=FONTB).grid(
                    row=10, column=0, columnspan=4)
                if self.stv.get():
                    tk.Label(self.fr, text="Output size : {}\nSize reduced : {}%".format(getSize(self.c.stats['outLen']), self.c.stats['compressionRate']), font=FONT).grid(row=11, column=0, columnspan=2)
                    tk.Button(self.fr, text="Show tree", command=self.showtree).grid(
                        row=11, column=2, columnspan=2)
            else:
                tk.Label(self.fr, text="Uncompression successful", font=FONTB).grid(
                    row=10, column=0, columnspan=4)
            self.bl.config(
                text="New File", command=self.reset, state=tk.NORMAL)
            return True
        self.state += 1
        self.win.after(100, self.process)

    def showtree(self):
        if self.comp:
            t = self.c.t
        else:
            t = tree(self.c.header)
        tktree("clic to quit", spacey=0, double=True).show(t)

    def reset(self):
        self.win.destroy()
        self = window()

    def stats(self, *args):
        self.bl.config(text="Launch")
        if self.stv.get() and self.comp and self.src != "":
            ext = self.src.split(".")[-1]
            ent = getEntropy(ext)
            pre = os.path.getsize(self.src)*(ent+min(ent+1,8))/16
            if pre != 0:
                self.bl.config(text="Launch (Est : "+getSize(pre)+")")

    def open(self):
        tmp = tkf.askopenfilename(
            title="Choose source file :", initialfile=self.srcv.get(), filetypes=self.srctypes)
        if tmp != "":
            self.src = tmp
            if self.comp:
                self.dst = self.src + ".clh"
            else:
                self.dst = self.src[:-4]
            self.check()

    def save(self):
        tmp = tkf.asksaveasfilename(
            title="Choose destination file :", initialfile=self.dstv.get(), filetypes=self.dsttypes)
        if tmp != "":
            self.dst = tmp
            self.check()

    def check(self):
        self.srcv.set(self.src.split("/")[-1])
        self.dstv.set(self.dst.split("/")[-1])
        if self.src != "" and self.dst != "":
            if os.path.getsize(self.src) >= 2**24:
                tkm.showerror("Size error", "Source file must be less than "+getSize(2**24))
                self.srcl.config(fg="red")
            else:
                self.bl.config(state=tk.NORMAL)
                self.srcl.config(fg=self.bl['fg'])
                self.stats()
        else:
            self.bl.config(state=tk.DISABLED)
            self.srcl.config(fg=self.bl['fg'])
            self.stats()


if __name__ == "__main__":
    window()

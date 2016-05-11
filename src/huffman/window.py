try:
    from .codec import codec
    from .tktree import tktree
    from .tree import tree
    from .entro import getEntropy
except SystemError:
    from codec import codec
    from tktree import tktree
    from tree import tree
    from entro import getEntropy
import tkinter as tk
import tkinter.filedialog as tkf
import tkinter.messagebox as tkm
import tkinter.ttk as ttk
import os

FONT = ("Helvetica", 10)
FONTB = ("Helvetica", 10, "bold")


def getSize(s):
    """
    Return a string telling the size of a file (in bytes)
    """
    if s < 10**3:
        return str(round(s, 2)) + " B"
    if s < 10**6:
        return str(round(s / 10**3, 2)) + " KB"
    if s < 10**9:
        return str(round(s / 10**6, 2)) + " MB"


class window:
    """
    Compression/decompression UI
    """
    def __init__(self):

        self.win = tk.Tk()
        self.win.title("Huffman")
        self.win.resizable(False, False)
        self.srcvar = tk.StringVar()
        self.dstvar = tk.StringVar()
        self.statvar = tk.BooleanVar()
        self.statvar.set(True)
        self.statvar.trace('w', self.stats)
        self.src = ""
        self.dst = ""
        self.srctypes = [('all files', '.*')]
        self.dsttypes = [('compressed file', '.clh'), ('all files', '.*')]
        self.comp = True
        self.launch = False
        self.source = ""
        self.state = 0
        self.progress = tk.IntVar(0)
        self.progress.trace('w', self.refresh)
        self.end = tk.IntVar()
        self.end.set(100)
        self.codec = codec(self.progress)
        self.win1()
        self.win.mainloop()

    def refresh(self, *args):
        """
        Refresh the window
        """
        self.win.update()

    def changemode(self):
        """
        Switch between compression and decompression mode
        """
        self.srctypes, self.dsttypes = self.dsttypes, self.srctypes
        self.comp = not self.comp
        self.srcvar.set("")
        self.dstvar.set("")
        self.butlaunch.config(state=tk.DISABLED)
        if self.comp:
            self.butmode.config(text="Compress")
        else:
            self.butmode.config(text="Uncompress")

    def win1(self):
        """
        Define the first part of the window content
        """
        self.frame = tk.Frame(self.win)

        tk.Label(self.frame, text="Mode : ", font=FONT).grid(
            row=0, column=0, sticky=tk.E)
        self.butmode = tk.Button(
            self.frame, text="Compress", width=28, command=self.changemode)
        self.butmode.grid(row=0, column=1, columnspan=3)

        self.srclab = tk.Label(self.frame, text="Source : ", font=FONT)
        self.srclab.grid(row=1, column=0, sticky=tk.E)
        tk.Entry(self.frame, textvariable=self.srcvar, width=30, state=tk.DISABLED).grid(
            row=1, column=1, columnspan=2)
        self.butsrc = tk.Button(self.frame, text=" ... ", command=self.open)
        self.butsrc.grid(row=1, column=3, sticky=tk.W)

        tk.Label(self.frame, text="Destination : ", font=FONT, width=10).grid(
            row=2, column=0, sticky=tk.E)
        tk.Entry(self.frame, textvariable=self.dstvar, width=30, state=tk.DISABLED).grid(
            row=2, column=1, columnspan=2)
        self.butdst = tk.Button(self.frame, text=" ... ", command=self.save)
        self.butdst.grid(row=2, column=3, sticky=tk.W)
        self.butstat = tk.Checkbutton(
            self.frame, text="show statistics", variable=self.statvar)
        self.butstat.grid(row=4, column=0, columnspan=2)
        self.butlaunch = tk.Button(self.frame, text="Launch", font=FONT,
                                   width=20, state=tk.DISABLED, command=self.process)
        self.butlaunch.grid(row=4, column=2, columnspan=2)

        self.frame.pack(padx=5, pady=5)

    def win2(self):
        """
        Define the second part of the window content
        """
        self.butsrc.config(state=tk.DISABLED)
        self.butdst.config(state=tk.DISABLED)
        self.butmode.config(state=tk.DISABLED)
        self.butlaunch.config(state=tk.DISABLED)
        self.butstat.config(state=tk.DISABLED)
        self.lab1 = tk.Label(self.frame, text="Loading : ", font=FONTB)
        self.lab1.grid(row=5, column=0, sticky=tk.E)
        self.prog1 = ttk.Progressbar(self.frame, length=200)
        self.prog1.grid(row=5, column=1, columnspan=2)
        self.lab2 = tk.Label(self.frame, text="Decoding : ", font=FONT)
        if self.comp:
            self.lab2.config(text="Encoding : ")
        self.lab2.grid(row=8, column=0, sticky=tk.E)
        self.prog2 = ttk.Progressbar(self.frame, length=200)
        self.prog2.grid(row=8, column=1, columnspan=2)
        self.lab3 = tk.Label(self.frame, text="Writing : ", font=FONT)
        self.lab3.grid(row=9, column=0, sticky=tk.E)
        self.prog3 = ttk.Progressbar(self.frame, length=200)
        self.prog3.grid(row=9, column=1, columnspan=2)

    def process(self):
        """
        Execute the compression/decompression
        """
        if self.state == 0:
            self.win2()
            self.prog1.config(variable=self.progress)
        elif self.state == 1:
            self.codec.load(self.src)
            self.lab1.config(font=FONT)
            self.lab2.config(font=FONTB)
            self.prog2.config(variable=self.progress)
            self.prog1.config(variable=self.end)
            if self.statvar.get():
                tk.Label(self.frame, text="{} s".format(
                    round(self.codec.stats['processTime'], 2)), font=FONT).grid(row=5, column=3)
        elif self.state == 2:
            if self.comp:
                self.codec.encode()
            else:
                self.codec.decode()
            self.lab2.config(font=FONT)
            self.lab3.config(font=FONTB)
            self.prog3.config(variable=self.progress)
            self.prog2.config(variable=self.end)
            if self.statvar.get():
                tk.Label(self.frame, text="{} s".format(
                    round(self.codec.stats['processTime'], 2)), font=FONT).grid(row=8, column=3)
        elif self.state == 3:
            self.codec.write(self.dst)
            self.lab3.config(font=FONT)
            if self.statvar.get():
                tk.Label(self.frame, text="{} s".format(
                    round(self.codec.stats['processTime'], 2)), font=FONT).grid(row=9, column=3)
        else:
            if self.comp:
                tk.Label(self.frame, text="Compression successful", font=FONTB).grid(
                    row=10, column=0, columnspan=4)
                if self.statvar.get():
                    tk.Label(self.frame, text="Output size : {}\nSize reduced : {}%".format(getSize(self.codec.stats[
                             'outLen']), self.codec.stats['compressionRate']), font=FONT).grid(row=11, column=0, columnspan=2)
                    tk.Button(self.frame, text="Show tree", command=self.showtree).grid(
                        row=11, column=2, columnspan=2)
            else:
                tk.Label(self.frame, text="Uncompression successful", font=FONTB).grid(
                    row=10, column=0, columnspan=4)
            self.butlaunch.config(
                text="New File", command=self.reset, state=tk.NORMAL)
            return True
        self.state += 1
        self.win.after(100, self.process)

    def showtree(self):
        """
        Show the tree window
        """
        if self.comp:
            t = self.codec.t
        else:
            t = tree(self.codec.header)
        tktree("clic to quit", spacey=0, double=True).show(t)

    def reset(self):
        """
        Make a new window for a new file
        """
        self.win.destroy()
        self = window()

    def stats(self, *args):
        """
        Set the statistic showing ON/OFF
        """
        self.butlaunch.config(text="Launch")
        if self.statvar.get() and self.comp and self.src != "":
            ext = self.src.split(".")[-1]
            ent = getEntropy(ext)
            pre = os.path.getsize(self.src) * (ent + min(ent + 1, 8)) / 16
            if pre != 0:
                self.butlaunch.config(
                    text="Launch (Est : " + getSize(pre) + ")")

    def open(self):
        """
        Select the file path of the source
        """
        tmp = tkf.askopenfilename(
            title="Choose source file :", initialfile=self.srcvar.get(), filetypes=self.srctypes)
        if tmp != "":
            self.src = tmp
            if self.comp:
                self.dst = self.src + ".clh"
            else:
                self.dst = self.src[:-4]
            self.check()

    def save(self):
        """
        Select the file path of the destination
        """
        tmp = tkf.asksaveasfilename(
            title="Choose destination file :", initialfile=self.dstvar.get(), filetypes=self.dsttypes)
        if tmp != "":
            self.dst = tmp
            self.check()

    def check(self):
        self.srcvar.set(self.src.split("/")[-1])
        self.dstvar.set(self.dst.split("/")[-1])
        if self.src != "" and self.dst != "":
            if os.path.getsize(self.src) >= 2**24:
                tkm.showerror(
                    "Size error", "Source file must be less than " + getSize(2**24))
                self.srclab.config(fg="red")
            else:
                self.butlaunch.config(state=tk.NORMAL)
                self.srclab.config(fg=self.butlaunch['fg'])
                self.stats()
        else:
            self.butlaunch.config(state=tk.DISABLED)
            self.srclab.config(fg=self.butlaunch['fg'])
            self.stats()


if __name__ == "__main__":
    window()

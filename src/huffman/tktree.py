import tkinter as tk
from tree import tree


class tktree:

    def __init__(self, title="", font=6, width=30):
        self.font = font
        self.width = width
        self.win = tk.Tk()
        self.win.title(title)
        self.cv = tk.Canvas(self.win, bg="white")
        self.cv.pack()

    def show(self, t, time=0):
        self.canv(t)
        if time > 0:
            self.win.after(time, self.win.quit)
        else:
            self.win.bind("<Button-1>", self.clic)
        self.win.mainloop()

    def clic(self, event):
        self.win.quit()

    def canv(self, t):
        self.cv.delete('all')
        l = len(t)
        s = t.getSize()
        h2 = self.font * 1.2
        w2 = self.width
        w = w2 * (2 * l + 1)
        h = h2 * (2 * s + 1)
        self.cv.config(width=w, height=h)
        genTreeH(self.cv, w2, h // 2, h, w2, h2, t)


def genTreeH(cv, x0, y0, dy, w2, h2, t):
    color = "white"
    if t.isLeaf:
        color = "yellow"
    cv.create_rectangle(
        x0, y0 - h2 // 2, x0 + w2, y0 + h2 // 2, outline="lightgrey", fill=color)
    cv.create_text(
        x0 + w2 / 2, y0, font=("Lucida console", int(h2 / 1.2)), text=repr(t))
    st = t.getSize()
    dy0 = y0 - dy // 2
    if not t.isLeaf:
        for child in t.children:
            hc = int(dy * child.getSize() / st)
            genTreeH(cv, x0 + w2 * 2, dy0 + hc // 2, hc, w2, h2, child)
            cv.create_line(
                x0 + w2, y0, x0 + w2 * 2, dy0 + hc // 2, fill="lightgrey")
            dy0 += hc

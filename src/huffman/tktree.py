import tkinter as tk
try:
    from . import leaf
except SystemError:
    import leaf

class tktree:

    def __init__(self, title="", font=6, width=30, height=1.2, spacex=0.5, spacey=0.5, double=False):
        self.font = font
        self.width = width
        self.win = tk.Tk()
        self.win.title(title)
        self.cv = tk.Canvas(self.win, bg="white")
        self.cv.pack()
        self.height = height
        self.spacex = spacex
        self.spacey = spacey
        self.double = double

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
        h2 = self.font * self.height
        w2 = self.width
        if not self.double:
            s = t.getSize()
            w = w2 * ((1 + self.spacex) * l + self.spacex)
            h = h2 * ((1 + self.spacey) * s + self.spacey)
            self.cv.config(width=w, height=h)
            genTreeH(self.cv, False, self.spacex, w2, h2, self.height, w2 * self.spacex,
                     self.spacey * h2 + h / 2, h, t)
        else:
            s = max(t.children[0].getSize(), t.children[1].getSize())
            w = w2 * ((1 + self.spacex) * l * 2 - self.spacex)
            h = h2 * ((1 + self.spacey) * s + self.spacey)
            self.cv.config(width=w, height=h)
            self.cv.create_line(w / 2 - w2 * 3 / 2 - self.spacex, self.spacey * h2 + h / 2,
                                w / 2 + w2 * 3 / 2 + self.spacex, self.spacey * h2 + h / 2,
                                fill="lightgrey")
            rect(self.cv, False, w2, h2, self.height, w / 2 - w2 / 2,
                 self.spacey * h2 + h / 2, h, t)
            genTreeH(self.cv, False, self.spacex, w2, h2, self.height,
                     w / 2 + w2 * (self.spacex + 1 / 2), self.spacey * h2 + h / 2, h, t.children[0])
            genTreeH(self.cv, True, self.spacex, w2, h2, self.height,
                     w / 2 - w2 * (self.spacex + 1 / 2), self.spacey * h2 + h / 2, h, t.children[1])


def genTreeH(cv, rev, spcx, w2, h2, fh, x0, y0, dy, t):
    rect(cv, rev, w2, h2, fh, x0, y0, dy, t)
    st = t.getSize()
    dy0 = y0 - dy / 2
    if not isinstance(t, leaf.leaf):
        for child in t.children:
            hc = int(dy * child.getSize() / st)
            if rev:
                genTreeH(cv, rev, spcx, w2, h2, fh, x0 - w2 *
                         (1 + spcx), dy0 + hc / 2, hc, child)
                cv.create_line(
                    x0 - w2, y0, x0 - w2 * (1 + spcx), int(dy0 + hc / 2), fill="lightgrey")
            else:
                genTreeH(cv, rev, spcx, w2, h2, fh, x0 + w2 *
                         (1 + spcx), dy0 + hc / 2, hc, child)
                cv.create_line(
                    x0 + w2, y0, x0 + w2 * (1 + spcx), int(dy0 + hc / 2), fill="lightgrey")
            dy0 += hc


def rect(cv, rev, w2, h2, fh, x0, y0, dy, t):
    color = "white"
    if isinstance(t, leaf.leaf):
        color = "yellow"
    if rev:
        x0 -= w2
    cv.create_rectangle(
        x0, int(y0 - h2 / 2), x0 + w2, int(y0 + h2 / 2), outline="lightgrey", fill=color)
    cv.create_text(
        int(x0 + w2 / 2), y0, font=("Lucida console", int(h2 / fh)), text=repr(t))

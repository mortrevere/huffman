import tkinter as tk
from tree import *
from leaf import *


def show(t, w, h):
    win = tk.Tk()
    cv = canv(win, t, w, h)
    cv.pack()
    win.mainloop()


def canv(parent, t, w, h):
    cv = tk.Canvas(parent, width=w, height=h, bg="white")
    wt = len(t)
    ht = t.getSize()
    print(wt)
    w2 = w // (2 * wt + 1)
    h2 = h // (2 * ht + 1)
    # Generate the visual tree recursively
    genTree(cv, w2, h // 2, h, w2, h2, t)
    return cv


def genTree(cv, x0, y0, dy, w2, h2, t):
    cv.create_rectangle(
        x0, y0 - h2 // 2, x0 + w2, y0 + h2 // 2, outline="lightgrey")
    cv.create_text(x0 + w2 / 2, y0, font=("Lucida console", 8), text=str(t))
    st = t.getSize()
    dy0 = y0 - dy // 2
    if not t.isLeaf:
        for child in t.children:
            hc = int(dy * child.getSize() / st)
            genTree(cv, x0 + w2 * 2, dy0 + hc // 2, hc, w2, h2, child)
            cv.create_line(
                x0 + w2, y0, x0 + w2 * 2, dy0 + hc // 2, fill="lightgrey")
            dy0 += hc
    return True  # TODO

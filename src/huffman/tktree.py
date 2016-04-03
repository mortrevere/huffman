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
    w2 = w // (2 * wt + 1)
    h2 = h // (2 * ht + 1)
    genTree(w2, h // 2, h, w2, h2, t)  # Generate the visual tree recursively
    return cv


def genTree(x0, y0, dy, w2, h2, t):
    return True  # TODO

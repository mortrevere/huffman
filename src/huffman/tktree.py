import tkinter as tk


def show(t, title, width=30, font=6):
    win = tk.Tk()
    win.title(title)
    cv = canv(win, t, width, font)
    cv.pack()
    win.mainloop()


def saveasimage(path, t, width=40, font=8):
    cv = canv(None, t, width, font)
    cv.postscript(file=path, colormode='color')


def canv(parent, t, w2, h2):
    l = len(t)
    s = t.getSize()
    h2 *= 1.1
    w = w2 * (2 * l + 1)
    h = h2 * (2 * s + 1)
    cv = tk.Canvas(parent, width=w, height=h, bg="white")
    genTreeH(cv, w2, h // 2, h, w2, h2, t)
    return cv


def genTreeH(cv, x0, y0, dy, w2, h2, t):
    color = "white"
    if t.isLeaf:
        color = "yellow"
    cv.create_rectangle(
        x0, y0 - h2 // 2, x0 + w2, y0 + h2 // 2, outline="lightgrey", fill=color)
    cv.create_text(
        x0 + w2 / 2, y0, font=("Lucida console", int(h2 / 1.1)), text=repr(t))
    st = t.getSize()
    dy0 = y0 - dy // 2
    if not t.isLeaf:
        for child in t.children:
            hc = int(dy * child.getSize() / st)
            genTreeH(cv, x0 + w2 * 2, dy0 + hc // 2, hc, w2, h2, child)
            cv.create_line(
                x0 + w2, y0, x0 + w2 * 2, dy0 + hc // 2, fill="lightgrey")
            dy0 += hc

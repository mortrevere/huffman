from codec import *
import tktree

c = codec()
c.load("a_very_short_story.txt")
tktree.show(c.t, 500, 500)

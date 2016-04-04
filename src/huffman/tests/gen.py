#! /usr/bin/python3.4
import random as r

for k in range(1, 32):
    name = "in/rand" + str(k) + ".txt"
    print("generating " + name + " weight:" + str(2**k) + " ...")
    with open(name, mode="wb") as f:
        f.write(bytes([r.randint(0, 255) for i in range(2**k)]))
print("generation done")

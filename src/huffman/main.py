#!/usr/bin/python3.4

from codec import *
from os import listdir
from os.path import isfile, join
files = [f for f in listdir('tests/') if isfile(join('tests/', f))]

for file in files:
    print(file)
    io = codec()

    io.load('tests/' + file)
    print("Loaded in : {}ms".format(io.stats['loadingTime'] * 1000))

    source = io.buf
    io.encode()
    print("Space saved : ", round(
        (1 - io.stats['outLen'] / io.stats['sourceLen']) * 100, 2), "%")
    print("Compressed in : {}ms".format(io.stats['processTime'] * 1000))

    io.decode()
    out = io.buf
    print("Decompressed in : {}ms".format(io.stats['processTime'] * 1000))

    print('Self-test result : ', end='')
    if source == out:
        print('ok')
    else:
        print('fail. \n\nDetails : ')
        if len(source) != len(out):
            delta = len(source) - len(out)
            common = min(len(source), len(out))
            print('\t /!\ Different length :\n\t\t Source :', len(source), '\n\t\t Output :', len(out),
                  '\n\t\t Difference :', delta)

            print('\t Difference on common length ({} bytes):'.format(common))
            if delta > 5:
                print('ur 2 fucked :(')
            else:
                for offset in range(0, delta + 1):
                    diff = 0
                    for i in range(common):
                        if delta < 0:
                            a = source[i]
                            b = out[i + offset]
                        else:
                            a = source[i + offset]
                            b = out[i]

                        if a != b:
                            diff += 1

                    print('\t\t offset {} : {}% ({} bytes)'.format(
                        offset, (diff / common) * 100, diff))
    print()

#!/usr/bin/python3.4

from codec import *
from os import listdir
from os.path import isfile, join
import sys

def sha1(filepath):
    import hashlib
    with open(filepath, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()

files = [f for f in listdir('tests/in/') if isfile(join('tests/in/', f))]

for file in files:
    path = 'tests/in/' + file
    tmp = 'tests/tmp/' + file + '.clz'
    out = 'tests/out/' + file

    io = codec()
    hIn = sha1(path)
    io.load(path)
    #print("Loaded in : {}ms".format(io.stats['loadingTime'] * 1000))
    print(io.stats['sourceLen'], ', ', end='', sep='')
    sys.stdout.flush()

    io.encode()
    #print("Compressed in : {}ms".format(io.stats['processTime'] * 1000))
    io.write(tmp,1)
    print(io.stats['compressionRate'])
    io.close()
    
    io.load(tmp)
    io.decode()
    #print("Decompressed in : {}ms".format(io.stats['processTime'] * 1000))
    io.write(out)
    io.close()
    hOut = sha1(out)
    
    #hOut = hIn
    #print('Self-test result : ', end='')
    if hIn == hOut:
        pass
        #print('ok')
    else:
        print('fail.')
        break
        #print('fail. \n\nDetails : ')
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
    #print()

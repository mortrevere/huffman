FILE = "entropy_data.dat"


def learnEntropy(datatype, entropy):
    data = loadData()
    d = data.get(datatype,(0, 0))
    data[datatype] = (
        (d[0] * d[1] + entropy) / (d[1] + 1), d[1] + 1)  # average
    saveData(data)


def getEntropy(datatype):
    return loadData()[datatype][0]


def loadData():
    data = {}
    open(FILE, 'a').close()  # create file if not exist
    with open(FILE, "r") as f:
        for line in f:
            d = line.strip().split(" ")
            if len(d) >= 3:
                data[d[0]] = (float(d[1]), int(d[2]))
    return data


def saveData(data):
    with open(FILE, "w") as f:
        for t in data.keys():
            f.write("{} {} {}\n".format(t, data[t][0], data[t][1]))

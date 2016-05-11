FILE = "entropy_data.dat"


def learnEntropy(datatype, entropy):
    """
    Save the entropy of the datatype for prediction
    """
    if datatype == "" or " " in datatype:
        return
    data = loadData()
    d = data.get(datatype,(0, 0))
    data[datatype] = (
        (d[0] * d[1] + entropy) / (d[1] + 1), d[1] + 1)  # average
    saveData(data)


def getEntropy(datatype):
    """
    Return the average entropy of the selected datatype if exist
    """
    if datatype == "":
        return 0
    return loadData().get(datatype,(0,0))[0]


def loadData():
    """
    Load entropy data from the selected file
    """
    data = {}
    open(FILE, 'a').close()  # create file if not exist
    with open(FILE, "r") as f:
        for line in f:
            d = line.strip().split(" ")
            if len(d) >= 3:
                data[d[0]] = (float(d[1]), int(d[2]))
    return data


def saveData(data):
    """
    Save entropy data in the selected file
    """
    with open(FILE, "w") as f:
        for t in data.keys():
            f.write("{} {} {}\n".format(t, data[t][0], data[t][1]))

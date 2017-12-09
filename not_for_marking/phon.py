import re
import matplotlib.pyplot as plt
with open ("phon.txt", "r") as f:
    f1di = 0
    f2di = 0
    f1dI = 0
    f2dI = 0
    f1de = 0
    f2de = 0
    f1ni = 0
    f2ni = 0
    f1nI = 0
    f2nI = 0
    f1ne = 0
    f2ne = 0
    lf1di = 0
    lf2di = 0
    lf1dI = 0
    lf2dI = 0
    lf1de = 0
    lf2de = 0
    lf1ni = 0
    lf2ni = 0
    lf1nI = 0
    lf2nI = 0
    lf1ne = 0
    lf2ne = 0
    for line in f.readlines():
        if "Dzhuen" in line and "i;" in line:
            f = re.search("(\d*?\\.\d*?);(\d*?\\.\d*?)", line)
            f1di += float(f.group(1))
            lf1di += 1
            f2di += float(f.group(2))
            lf2di += 1
        if "Dzhuen" in line and "I;" in line:
            f = re.search("(\d*?\\.\d*?);(\d*?\\.\d*?)", line)
            f1dI += float(f.group(1))
            lf1dI += 1
            f2dI += float(f.group(2))
            lf2dI += 1
        if "Dzhuen" in line and "e;" in line:
            f = re.search("(\d*?\\.\d*?);(\d*?\\.\d*?)", line)
            f1de += float(f.group(1))
            lf1de += 1
            f2de += float(f.group(2))
            lf2de += 1
        if "Naikhin" in line and "i;" in line:
            f = re.search("(\d*?\\.\d*?);(\d*?\\.\d*?)", line)
            f1ni += float(f.group(1))
            lf1ni += 1
            f2ni += float(f.group(2))
            lf2ni += 1
        if "Naikhin" in line and "I;" in line:
            f = re.search("(\d*?\\.\d*?);(\d*?\\.\d*?)", line)
            f1nI += float(f.group(1))
            lf1nI += 1
            f2nI += float(f.group(2))
            lf2nI += 1
        if "Naikhin" in line and "e;" in line:
            f = re.search("(\d*?\\.\d*?);(\d*?\\.\d*?)", line)
            f1ne += float(f.group(1))
            lf1ne += 1
            f2ne += float(f.group(2))
            lf2ne += 1
    f1di = f1di /lf1di
    f2di = f2di / lf2di
    f1dI = f1dI / lf1dI
    f2dI = f2dI / lf2dI
    f1de = f1de / lf1de
    f2de = f2de / lf2de
    f1ni = f1ni / lf1ni
    f2ni = f2ni / lf2ni
    f1nI = f1nI / lf1nI
    f2nI = f2nI / lf2nI
    f1ne = f1ne / lf1ne
    f2ne = f2ne / lf2ne
    X = [f1di, f1dI, f1de, f1ni , f1nI, f1ne ]
    Y = [f2di, f2dI, f2de, f2ni , f2nI, f2ne]
    size = [20, 20, 20, 50, 50, 50]
    colors = ['red', 'green',  'blue', 'red', 'green', 'blue']
    plt.scatter(X, Y, s = size, c= colors, marker = '^')
    plt.show()

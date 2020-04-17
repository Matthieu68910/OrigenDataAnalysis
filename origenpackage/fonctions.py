import os

import matplotlib.pyplot as plt


class Result:
    def __init__(self, i = 'NaN', l = 0, t = 'NaN', v = []):
        self.isotope = i
        self.line = l
        self.type = t
        self.value = v

    def getValue(self):
        return self.value

    def getIsotope(self):
        return self.isotope

    def getType(self):
        return self.type

    def getLine(self):
        return self.line

    def setIsotope(self, string):
        self.isotope = string

    def setLine(self, int):
        self.line = int

    def setType(self, string):
        self.type = string

    def setValue(self, value):
        for val in value:
            self.value.append(val)

    def printResult(self):
        print("Isotope : " + str(self.isotope))
        print("Type : " + str(self.type))
        print("Ligne : " + str(self.line))
        print("Valeurs : ")
        print(self.value)
        print("\n")

    def returnResult(self):
        text = "Isotope : " + str(self.isotope) + "\nType : " + str(self.type) + "\nDatas : " + str(self.value)
        return text


def plotfig(charge, resultat, width=9.9, height=5, res=100, log=True, process=False):
    # print("Log, at start of plotfig : " + str(log))
    lab = resultat.getType()
    mas = resultat.getValue()

    '''if process and max(mas) != 0:
        if (min(mas) / max(mas)) < 0.01:
            log = True
        else:
            log = False'''

    plt.figure(figsize=(width, height), dpi=res)
    # plt.plot(charge, mas, label=lab)
    axes = plt.gca()
    if log:
        plt.yscale('log')
        if min(mas) == 0:
            axes.set_ylim([(min(mas) - (0.1 * min(mas))) + 0.00001, (max(mas) + (0.1 * max(mas)))])
        else:
            axes.set_ylim([(0.1 * min(mas)), (10 * max(mas))])
    else:
        plt.yscale('linear')
        axes.set_ylim([(min(mas) - (0.1 * min(mas))), (max(mas) + (0.1 * max(mas)))])
    plt.plot(charge, mas, label=lab)
    pretitle = resultat.getIsotope()
    pretitle1 = pretitle[0].upper() + pretitle[1:].lower()
    title = pretitle1 + ' - ' + lab
    plt.axvline(600, 0, 1, label='Reactor stopped', color='g')
    plt.title(title)
    plt.xlabel("Duration [days]")
    if lab == "(Alpha, N)" or lab == "Spontaneous Fiss. N. Source":
        plt.ylabel("Neutrons / sec")
    else:
        plt.ylabel("Mass [g]")
    plt.legend()
    return plt


def readfile(path):
    mylines = []  # lines of the file
    balise = [[], [], [], [], []]  # balise au format (1000 + line)
    chargenum = []  # vecteur de float reprenant le nombre de jours
    with open(path, "rt") as myfile:  # file read
        for myline in myfile:
            mylines.append(myline)
        for x in range(len(mylines)):  # localisation of strips
            if mylines[x].find("ACTIVATION PRODUCT", 98, 120) != -1:
                balise[0].append(x)
            elif mylines[x].find("ACTINIDES+DAUGHTERS", 98, 120) != -1:
                balise[1].append(x)
            elif mylines[x].find("FISSION PRODUCTS", 98, 120) != -1:
                balise[2].append(x)
            elif mylines[x].find("(ALPHA,N)", 27, 40) != -1:
                balise[3].append(x)
            elif mylines[x].find("FISSION NEUTRON SOURCE", 40, 65) != -1:
                balise[4].append(x)
            else:
                pass
        for y in range(len(mylines)):  # recovery of CHARGE
            if mylines[y].find("CHARGE", 10, 20) != -1:
                line = mylines[y].replace("CHARGE", '')
                charge = line.split()
                for z in range(len(charge)):
                    if charge[z].find('D') != -1:
                        a = charge[z].replace("D", '')
                        chargenum.append(float(a))
                    elif charge[z].find('YR') != -1:
                        a = charge[z].replace("YR", '')
                        chargenum.append((float(a) * 365) + 600)
                break
        if not os.path.exists("Data"):
            os.mkdir("Data")
        f = open("Data/data.txt", "w+")
        for z in range(len(mylines)):
            if balise[0][0] <= z <= balise[1][0]:
                if mylines[z][1:3] != "  " and mylines[z][0:6] != "ORIGEN" and mylines[z] != "\n":
                    isotope = mylines[z][0:10].replace(' ', '')
                    value = mylines[z][10:].split()
                    f.write(isotope + "\nActivation Products\n")
                    for x in value:
                        f.write(str(x) + ", ")
                    f.write("\n")
            if balise[1][0] <= z <= balise[2][0]:
                if mylines[z][1:3] != "  " and mylines[z][0:6] != "ORIGEN" and mylines[z] != "\n":
                    isotope = mylines[z][0:10].replace(' ', '')
                    value = mylines[z][10:].split()
                    f.write(isotope + "\nActinides + Daughters\n")
                    for x in value:
                        f.write(str(x) + ", ")
                    f.write("\n")
            if balise[2][0] <= z <= balise[3][0]:
                if mylines[z][1:3] != "  " and mylines[z][0:6] != "ORIGEN" and mylines[z] != "\n":
                    isotope = mylines[z][0:10].replace(' ', '')
                    value = mylines[z][10:].split()
                    f.write(isotope + "\nFission Products\n")
                    for x in value:
                        f.write(str(x) + ", ")
                    f.write("\n")
            if balise[3][0] <= z <= balise[4][0]:
                if mylines[z][1:3] != "  " and mylines[z][0:6] != "ORIGEN" and mylines[z] != "\n" and mylines[z][
                                                                                                      0:3] != "---" and \
                        mylines[z][0:6] != "TOTALS" and mylines[z][0:6] != "OVERAL":
                    isotope = mylines[z][0:10].replace(' ', '')
                    value = mylines[z][10:].split()
                    f.write(isotope + "\n(Alpha, N)\n")
                    for x in value:
                        f.write(str(x) + ", ")
                    f.write("\n")
            if balise[4][0] < z:
                if mylines[z][1:3] != "  " and mylines[z][0:6] != "ORIGEN" and mylines[z] != "\n" and mylines[z][
                                                                                                      0:3] != "---" and \
                        mylines[z][0:6] != "TOTALS" and mylines[z][0:6] != "OVERAL":
                    isotope = mylines[z][0:10].replace(' ', '')
                    value = mylines[z][10:].split()
                    f.write(isotope + "\nSpontaneous Fiss. N. Source\n")
                    for x in value:
                        f.write(str(x) + ", ")
                    f.write("\n")
        f.close()
    return chargenum




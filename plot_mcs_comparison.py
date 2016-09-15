import matplotlib.pyplot as plt
import csv
import numpy as np
import re

##############################################################################################################
#                                            Configuration                                                   #
############################################################################################################## 
DIR_1 = "MU-MIMO-Characterization/2SS_Characterization/Default-Image/MU-Enabled"
FILE_NAME_1 = "3MU_2SS-end.dat"
LABEL_1 = "Default"

DIR_2 = "MU-MIMO-Characterization/2SS_Characterization/MuseRC-Image/"
FILE_NAME_2 = "3MU_2SS-end.dat"
LABEL_2 = "MuseRate"

COLOR_1 = "#8899ff"
COLOR_2 = "#ff9922"

TITLE = ""
XTICKS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
BAR_WIDTH = 0.25
BAR_SPACING = 0.05

##############################################################################################################
def getmcs(filename, DIR):
    f = open(DIR + "/" + filename)     
    mcs = []
    for line in f:
        if "VHT Tx TxBF counts(0..9)" in line:
            mcs = line.split(":")[1].split(",")

    for i in range(len(mcs)):
        if len(mcs[i]) == 0:
            mcs.remove(i)
        else:
            mcs[i] = int(mcs[i])

    # Normalize MCS Counts
    total = sum([i for i in mcs])
    mcs = [float(i)/float(total) for i in mcs]

    return mcs
##############################################################################################################

mcs_1 = getmcs(FILE_NAME_1, DIR_1)
mcs_2 = getmcs(FILE_NAME_2, DIR_2)

print mcs_1
print mcs_2

N = 10

ind = np.array(range(N))    # the x locations for the groups


plt.style.use("ggplot")

p1 = plt.bar(ind, [mcs_1[j] for j in range(N)], BAR_WIDTH, color=COLOR_1)

p2 = plt.bar(ind+BAR_WIDTH+BAR_SPACING, [mcs_2[j] for j in range(N)], BAR_WIDTH, color=COLOR_2)

plt.ylabel('Ratio')
plt.xlabel('MCS')
plt.title(TITLE)

plt.xlim(-BAR_SPACING, (N-1) + 2*(BAR_WIDTH+BAR_SPACING))
plt.xticks(ind + BAR_SPACING/2.0 + BAR_WIDTH, (XTICKS))

plt.legend((p1, p2), (LABEL_1, LABEL_2), loc = "upper left")

plt.show()
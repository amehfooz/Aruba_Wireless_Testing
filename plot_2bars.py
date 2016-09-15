import matplotlib.pyplot as plt
import csv
import numpy as np

##############################################################################################################
#                                            Configuration                                                   #
############################################################################################################## 
DIR_1 = "2MU_2SS_MU/Test-1"
FILE_NAMES_1 = ["2MU_2SS"]
LABEL_1 = "MU"

DIR_2 = "Test-1"
FILE_NAMES_2 = ["2MU_2SS"]
LABEL_2 = "MU-Updated"

COLOR_1 = "#8899ff"
COLOR_2 = "#ff9922"

XAXIS_LABEL = ""
YAXIS_LABEL = ""

# Number of Runs to plot over
RUNS = 3

TITLE = ""
XTICKS = ["2", "8", "15"]
BAR_WIDTH = 0.25
BAR_SPACING = 0.05


##############################################################################################################
def getmeans(files, DIR):
    results = [[], [], [], [] ,[] ,[], [], [], [], [], [], [] ,[], []]

    print results

    for j in range(len(files)):
        for i in range(1, RUNS+1):
            f = open(DIR + "/" + files[j] + str(i) + ".zip.csv")     
            results[j] += [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]

    y = []
    num_mixes = [1] * len(files)

    for j in range(len(files)):
        y.append([int(a['Throughput']) / 2**20 for a in results[j]])       
    means = []
    [means.append(np.mean(i[2:])) for i in y]
    
    return means
##############################################################################################################

if len(FILE_NAMES_1) != len(FILE_NAMES_2):
    print "Need equal number of files for comparison"
    exit()

means_1 = getmeans(FILE_NAMES_1, DIR_1)
means_2 = getmeans(FILE_NAMES_2, DIR_2)

N = len(FILE_NAMES_1)

ind = np.array(range(N))    # the x locations for the groups


plt.style.use("ggplot")

p1 = plt.bar(ind, [int(means_1[j]) for j in range(N)], BAR_WIDTH, color=COLOR_1)

p2 = plt.bar(ind+BAR_WIDTH+BAR_SPACING, [means_2[j] for j in range(N)], BAR_WIDTH, color=COLOR_2)

plt.ylabel(YAXIS_LABEL)
plt.xlabel(XAXIS_LABEL)
plt.title(TITLE)

plt.xlim(-BAR_SPACING, (N-1) + 2*(BAR_WIDTH+BAR_SPACING))
plt.xticks(ind + BAR_SPACING/2.0 + BAR_WIDTH, (XTICKS))

plt.legend((p1, p2), (LABEL_1, LABEL_2), loc = "upper left")

plt.show()
#!python3
# -*- coding: utf-8 -*-

# import
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
import time

# CAM's LAYOUT

SMALL_SIZE = 24
BIGGER_SIZE = 32
plt.rcParams.update({'font.size': SMALL_SIZE,
                     'axes.titlesize': BIGGER_SIZE,
                     'axes.edgecolor': 'black',
                     'axes.labelsize': BIGGER_SIZE,
                     'axes.linewidth': 3,
                     'xtick.labelsize': SMALL_SIZE,
                     'xtick.major.size': 10,
                     'xtick.major.width': 3,
                     'lines.markersize': 2,
                     'patch.linewidth': 3.0,
                     'ytick.labelsize': SMALL_SIZE,
                     'ytick.major.size': 10,
                     'ytick.major.width': 2,
                     'ytick.minor.size': 6,
                     'ytick.minor.width': 1})
plt.rcParams['axes.xmargin'] = 0

# Timing

start_time = time.time()

# Lists
pos_K_in_file, val_K, pos_K_in_plot = ([] for _ in range(3))


# File
print("reading the header")
with open('BAND-80K.DAT','r') as f:
    line = f.readline()
    NKPT = int(line.split()[2]) #number of KPOINTS
    NBDN = int(line.split()[4]) #number of bands
    NSPIN = int(line.split()[6]) #number of spin
    while "NPANEL" not in line:
        line = f.readline()
    line = f.readline()
    while "@" not in line:
        pos_K_in_file.append(int(line.split()[1]))
        val_K.append(str(line.split()[2]))
        line = f.readline()


# filecleaned is a generator to ignore # and @ in files
filecleaned = (r for r in open('BAND-80K.DAT') if not r[0] in ('@', '#'))

# file
print("reading the file, please wait")
DATA = np.genfromtxt(filecleaned, delimiter="")

# convert energy in eV
eV = 27.21
DATA_eV_all = np.multiply(DATA, eV)


# replace the correct KPOINTSnumbers
DATA_KPTS = np.divide(DATA_eV_all[:,0], eV)
#print(np.shape(DATA_eV_all))

for i in pos_K_in_file:
    pos_K_in_plot.append(DATA_KPTS[i-1])
   
fig1, ax1 = plt.subplots()
ax1.axhline(y = 0, xmin = 0, xmax = max(pos_K_in_plot),lw = 2,  linestyle = "--", color = "k")

for i in range(1,NBDN+1): #place the K POINTS
   # ax1.plot(DATA_KPTS, DATA_eV_all[:,i], color="k", lw = 3,)
    ax1.scatter(DATA_KPTS, DATA_eV_all[:,i], marker = "o")
ax1.set_xlabel("KPOINTS Path")
ax1.set_ylabel(r"Energy ($E-E_F$) in eV")
plt.xticks(pos_K_in_plot,val_K)
print("--- %s seconds ---" % (time.time() - start_time))

plt.show()



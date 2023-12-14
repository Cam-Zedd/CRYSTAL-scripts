#!python3
# -*- coding: utf-8 -*-

# import
import matplotlib
import matplotlib.pyplot as plt
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
                     'xtick.major.width': 2,
                     'lines.markersize': 10,
                     'patch.linewidth': 3.0,
                     'ytick.labelsize': SMALL_SIZE,
                     'ytick.major.size': 10,
                     'ytick.major.width': 2,
                     'ytick.minor.size': 6,
                     'ytick.minor.width': 1})
plt.rcParams['axes.xmargin'] = 0

# Timing

start_time = time.time()

# File


DATA = np.genfromtxt('DOSS.DAT',
        delimiter="",
        skip_header=4,
        skip_footer=1)  # , skiprows=4503)


DATA_EV = 27.21 * DATA[:, 0]
valtot = np.shape(DATA)[1] - 1
fig1, ax1 = plt.subplots()

ax1.plot(DATA_EV, DATA[:, valtot], label="tot", lw=3)
ax1.plot(DATA_EV, DATA[:, 2], label="Ti/2", lw=3)
ax1.plot(DATA_EV, DATA[:, 3], label="O/4", lw=3)
ax1.legend(loc='best', frameon=False)
# ax1.set_ylim(0,1.05)
ax1.set_xlabel(r"$E - E_F$ (eV)")
ax1.set_ylabel(r"Density of States")

print("--- %s seconds ---" % (time.time() - start_time))

# Plot

plt.show()

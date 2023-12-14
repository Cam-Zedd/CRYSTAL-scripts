#!python3
# -*- coding: utf-8 -*-

# import
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
                     'xtick.major.width': 3,
                     'lines.markersize': 3,
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
filename = 'log.446669'

# The code 
print("parsing the file")
print("")
print("")
print("#############################################################")
print("")
print("")
# STACK the number of bands to read

with open(filename,'r') as f:
    line = f.readline()
	
    while "DISPERSION K POINT NUMBER" not in line:
        line = f.readline()
    line = f.readline()
    while "DISPERSION K POINT NUMBER" not in line:	
        if ")" in line:
            NUMBER_of_BANDS = int(line.split()[1])
        line = f.readline()
print(f"{NUMBER_of_BANDS} bands found")
print("")

# Prepare the nested lists 
# number of list is the number of bands to be plotted

ENERGYcm =[ [] for _ in range(NUMBER_of_BANDS) ]

# Stack all the values in function of the number of K POINTS. 
with open(filename,'r') as f:
	line = f.readline()
	while "DISPERSION K POINT NUMBER" not in line: # go directly to the first case to escape exceptions
		line = f.readline()
	line = f.readline()
	while "END" not in line: # end point for the data
		line = f.readline()
		if "NUMBER OF K POINTS:" in line:
			KPOINTS_PER_SEGMENT = int(line.split("NUMBER OF K POINTS:")[1])
		for i in range(NUMBER_of_BANDS): #assign data with respect to the bands
			if f" {i+1}-  " in line:
				#print(line.split())
				ENERGYcm[i].append(float(line.split()[3]))			
print(f"{KPOINTS_PER_SEGMENT} KPOINTS per segment were found")
print("")
print(f"{len(ENERGYcm[0])} KPOINTS found for the first band") 
print("")
SEGMENT_NUMBER = (len(ENERGYcm[0]))/KPOINTS_PER_SEGMENT
SEGMENT_NUMBER = int(SEGMENT_NUMBER)
print(f"{SEGMENT_NUMBER} segments were found")
print("")
print("")
print("#############################################################")
KPOINTS_NUMBER = np.arange(0,len(ENERGYcm[0])) # numerote the KPOINTS numbers
ENERGYcm = np.array(ENERGYcm) # convert in numpy array to be transposed the values 
TENERGYcm = ENERGYcm.transpose() # transpose to avoid a double enumerate loop and speed up the process

fig1, ax1 = plt.subplots() # plot along the K points in function of the band
for i in range(NUMBER_of_BANDS):
	ax1.plot(KPOINTS_NUMBER,TENERGYcm[:,i], "o-", )

#xticks = np.arange(0,len(ENERGYcm[0])+1,KPOINTS_PER_SEGMENT)
xticks = []
for i in range(0,len(ENERGYcm[0])+1,KPOINTS_PER_SEGMENT):
	xticks.append(i)
xticks[-1] = xticks[-1] - 1 

labname = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"][:len(xticks)]
plt.xticks(xticks,labname)

plt.xlim(0,len(ENERGYcm[0])-1)
ax1.set_box_aspect(1)
ax1.set_xlabel("KPOINTS Path")
ax1.set_ylabel(r"Energy (cm$^{-1}$)")	

print("--- %s seconds ---" % (time.time() - start_time))	

plt.show()	


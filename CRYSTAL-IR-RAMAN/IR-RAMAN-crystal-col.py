#!python3
# -*- coding: utf-8 -*-

'''
Code to plot IR and RAMAN from CRYSTAL 

###### What you need to modify ####

filetoparser = files to be read (list)
name = names to give in the plot (list)
sigma or valsigma = value for gaussian/lorentzian shapes 

'''

# Modules

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import time

######### Timings #########

start_time = time.time()

######## CAM's LAYOUT #########

SMALL_SIZE = 24
BIGGER_SIZE = 32
plt.rcParams.update({'font.size': SMALL_SIZE,
                     'axes.titlesize': BIGGER_SIZE,
                     'axes.edgecolor': 'black',
                     'axes.labelsize': BIGGER_SIZE,
                     'axes.linewidth': 2,
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


######### FILES TO BE READ #########

#filetoparser = ["job.out", "IR.log"]
filetoparser = ["log.PBE446328", "log.PBE0446657", "MgO.log", "IR.log", "TiO2_rutile.log"]

######### COMPOUND NAMES #########

#name = [r"$TiO_2$", r"$TiO_2$ IR"]
name = [r"PBE", r"PBE0", r"Mgo", r"IR-alone", r"TiO2_rutile"]

######### START THE LISTS #########

energycm, intensity, intens, energyRaman, intensityRamanTot, intensityRamanPar, intensityRamanPerp, maxintensity, maxintensityRamanTot, mincm, maxcm, minraman, maxraman = (
    [[]for _ in range(len(filetoparser))] for _ in range(13))

######### Colors #########

c = [
    "dodgerblue",
    "coral",
    "seagreen",
    "darkorchid",
    "red",
    "dimgrey",
    "orangered",
    "peru",
    "limegreen",
    "slateblue",
    ]

######### Gaussian function #########

def spec(E, f, sigma, x):
    E = np.array(E)
    f = np.array(f)
    x = np.array(x)

    # Compute the spectrum using vectorized operations
    delta_E = (E - x[:, np.newaxis]) / sigma
    spectrum = np.sum(f * np.exp(-delta_E**2), axis=1)

    return spectrum

def plot_lorentzian(E, f, sigma, x):
    E = np.array(E)
    f = np.array(f)
    x = np.array(x)
    spectrum_lz = np.sum(f / np.pi * sigma / ((E - x[:, np.newaxis])**2 + sigma**2), axis=1)
    return spectrum_lz

sigma = 3
valsigma = [10, 10]
num = 5000 #linspace



######### FILES TO BE READ #########

fig3, ax3 = plt.subplots()  # IR
fig1, ax1 = plt.subplots()  # RAMAN

for i in range(len(filetoparser)):
    with open(filetoparser[i], 'r') as f:  # FIRST for IR
        line = f.readline()
        while "CONVERSION FACTORS FOR FREQUENCIES" not in line:
            line = f.readline()
            # print(line) #parse all the lines
        line = f.readline()
        # print(line) #now in line CONVERSION ...
        while "(KM/MOL)" not in line:
            line = f.readline()  # one more to get the first value
        line = f.readline()
        while not line.isspace():  # seek the space
            beg, _, end = line.split('(')
            energycm[i].append(float(beg.split()[3]))
            intensity[i].append(float(end[:9]))
            line = f.readline()
        line = f.readline()

        print("")
        print("for file", filetoparser[i])
        for j, k, in zip(energycm[i], intensity[i]):
            print("{:.4f}".format(j), "cm-1 |",
                  "I_tot: ", "{:.2f}".format(k))
        mincm[i] = min(energycm[i])
        maxcm[i] = max(energycm[i])
        maxintensity[i] = max(intensity[i])
        x = np.linspace(0.01, maxcm[i]*1.2, num)
        print("for file", filetoparser[i], "named", name[i])
        print("Starting to plot IR")
        spectrum = spec(energycm[i], intensity[i], sigma, x)
        ax3.plot(
            x,
            spectrum /
            np.max(spectrum),
            "-",
            label=f"{name[i]}",
            color=c[i],
            lw=3)
        print(
            f"IR spectrum of {name[i]} achieved in :"
            "%s seconds" %
            (time.time() - start_time))
        # Store csv
        fname = filetoparser[i]
        with open(f"{fname}-IR.csv", "w") as g:
            g.write("E(cm-1),I")
            for o in range(num):
                g.write(f'\n{x[o]},{spectrum[o]/spectrum.max()}')

        if "<RAMAN>" in line:  # RAMAN
            line = f.readline()
            print("starting to index RAMAN for file", filetoparser[i])
            while "-------------------------------------------------------" not in line:
                # print(line)
                line = f.readline()
            line = f.readline()
            while not line.isspace():
                energyRaman[i].append(float(line.split()[2]))
                intensityRamanTot[i].append(float(line.split()[-3]))
                intensityRamanPar[i].append(float(line.split()[-2]))
                intensityRamanPerp[i].append(float(line.split()[-1]))
                line = f.readline()
            print("values of Raman intensity : ")
            # A faire : for a,b,c,d in 4 lists. Le plot. Les prints avec df.

            # Starting RAMAN
            if energyRaman[i]:
                for j, k, l, m in zip(energyRaman[i], intensityRamanTot[i],
                                      intensityRamanPar[i], intensityRamanPerp[i]):
                    print("{:.4f}".format(j), "cm-1 |",
                          "I_tot: ", "{:.2f}".format(k),
                          "  I_par: ", "{:.2f}".format(l),
                          "  I_perp: ", "{:.2f}".format(m))
                minraman[i] = min(energyRaman[i])
                maxraman[i] = max(energyRaman[i])
                maxintensityRamanTot[i] = max(intensityRamanTot[i])
                x = np.linspace(0.01, maxraman[i]*1.2, num)
                print("for file", filetoparser[i], "named", name[i])
                print("Starting to plot RAMAN")
                spectrum = spec(energyRaman[i], intensityRamanTot[i], sigma, x)
                ax1.plot(
                    x,
                    spectrum /
                    np.max(spectrum),
                    "-",
                    label=f"{name[i]}",
                    color=c[i],
                    lw=3)
                spectrum_lz =plot_lorentzian(energyRaman[i], intensityRamanTot[i], sigma, x)     
                # Lorentzian
                ax1.plot(
                    x,
                    spectrum_lz /
                    np.max(spectrum_lz),
                    "--",
                    label=f"{name[i]}-L",
                    color=c[-i],
                    lw=3)
                 
                print(f"RAMAN spectrum of {name[i]} achieved in :"
                      "%s seconds" % (time.time() - start_time))
                print(len(filetoparser))
                with open(f"{filetoparser[i]}-RAMAN.csv", "w") as g:
                    g.write("E(cm-1),I(Gau),I(Lor)")
                    for o in range(num):
                        g.write(f'\n{x[o]},{spectrum[o]/spectrum.max()},{spectrum_lz[o]/spectrum_lz.max()}')
            else:
                print("######## no RAMAN ########")
        else:
            print("######## no RAMAN ########")
#remove empty elemets
maxcm = list(filter(None, maxcm))
maxraman = list(filter(None, maxraman))


#limits
ax3.legend(loc='upper left', frameon=False)
ax3.set_xlim(0, max(maxcm)*1.1)
ax3.set_ylim(0, 1.05)
ax3.set_xlabel(r"Energy (cm$^{-1}$)")
ax3.set_ylabel(r"Normalized Intensity")

ax1.legend(loc='upper left', frameon=False)
ax1.set_xlim(0, max(maxraman)*1.1)
ax1.set_ylim(0, 1.05)
ax1.set_xlabel(r"RAMAN shift (cm$^{-1}$)")
ax1.set_ylabel(r"Normalized Intensity")

print("--- The process took %s seconds ---" % (time.time() - start_time))


plt.show() 
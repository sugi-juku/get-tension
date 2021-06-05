#!/usr/bin/env python3
# coding: utf-8

import csv
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

import string_data as sda
import string_rec as sre
import string_lr as slr

for key, name in sda.stdata_file.items():
    x=[]
    y=[]
    with open(name) as csvf:
        reader = csv.reader(csvf)
        header = next(reader)
        # print(header)
        i = 0
        for row in reader:
            sdata = sda.StringData(row)
            i += 1
            # Frequency
            x.append(sdata.get_f0())
            # Tension
            y.append(sdata.get_tension())
        sample_n = int(i/sre.REC_N)
    # Show graph
    plt.title(sda.sname[key] + " Stringing Data " + str(sample_n))
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Tension (lbs)")
    plt.scatter(x, y)
    pf1 = np.polyfit(x, y, 1)
    pf1_a = round(pf1[0], 4)
    pf1_b = round(pf1[1], 3)
    if pf1_b < 0:
        pf1_str = f"y={pf1_a}x{pf1_b}"
    else:
        pf1_str = f"y={pf1_a}x+{pf1_b}"
    func = np.poly1d(np.polyfit(x, y, 1))
    x.sort()
    plt.plot(x, func(x), label=f"Polyfit {pf1_str}")
    plt.legend()
    plt.show()

    # Calculate mean squared error
    error2 = 0.0
    err = []
    for i,x_val in enumerate(x):
        error = y[i] - func(x_val)
        error2 += error*error
        err.append(error)
    mean_squared_error = error2/len(x)
    mse_msg = "y=ax+b Mean squared error = " + str(round(mean_squared_error,2))
    print(mse_msg)
 
    # Show graph
    plt.title(sda.sname[key] + f" Polyfit {pf1_str} Error")
    plt.xlabel("Error (lbs)")
    plt.ylabel("Tension (lbs)")
    plt.scatter(err, y, label=mse_msg)
    plt.legend()
    plt.show()

    # LR Data
    stglr = slr.StringLr01(key)
    stglr.fit()
    mean_squared_error = stglr.get_mean_squared_error()
    mse_msg = "LR Mean squared error = " + str(round(mean_squared_error,2))
    print(mse_msg)

    if key == "T":
        check_val = 4
    else:
        check_val = 2

    for i,val in enumerate(stglr.error):
        if abs(val) > check_val:
            print(i+2,val)

    # Show graph
    plt.title(sda.sname[key] + " LR Error")
    plt.xlabel("Error (lbs)")
    plt.ylabel("Tension (lbs)")
    plt.scatter(stglr.error, stglr.y, label=mse_msg)
    plt.legend()
    plt.show()


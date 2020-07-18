#!/usr/bin/env python3
# coding: utf-8

import csv
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

import string_data as sd
import string_lr as sl

for key, name in sd.stdata_file.items():
    x=[]
    y=[]
    with open(name) as csvf:
        reader = csv.reader(csvf)
        header = next(reader)
        # print(header)
        i = 0
        for row in reader:
            sdata = sd.StringData(row)
            i += 1
            # Frequency
            x.append(sdata.get_f0())
            # Tension
            y.append(sdata.get_tension())
        sample_n = int(i/2)
    # Show graph
    plt.title(sd.sname[key] + " Stringing Data " + str(sample_n))
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Tension (Lbs)")
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
    plt.title(sd.sname[key] + f" Polyfit {pf1_str} Error")
    plt.xlabel("Error (Lbs)")
    plt.ylabel("Tension (Lbs)")
    plt.scatter(err, y, label=mse_msg)
    plt.legend()
    plt.show()

    # LR Data
    slr = sl.StringLr00(key)
    slr.fit()
    mean_squared_error = slr.get_mean_squared_error()
    mse_msg = "LR Mean squared error = " + str(round(mean_squared_error,2))
    print(mse_msg)
 
    # Show graph
    plt.title(sd.sname[key] + " LR Error")
    plt.xlabel("Error (Lbs)")
    plt.ylabel("Tension (Lbs)")
    plt.scatter(slr.error, slr.y, label=mse_msg)
    plt.legend()
    plt.show()


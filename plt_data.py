#!/usr/bin/env python
# coding: utf-8

import csv
import os
import numpy as np
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import string_data as sd
import string_lr as sl

for key, name in sd.stdata_file.items():
    x=[]
    y=[]
    with open(name) as csvf:
        reader = csv.reader(csvf)
        header = next(reader)
        # print(header)
        for row in reader:
            sdata = sd.StringData(row)
            # Frequency
            x.append(sdata.get_f0())
            # Tension
            y.append(sdata.get_tension())

    # Show graph
    plt.title(sd.sname[key] + " Stringing Data")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Tension (Lbs)")
    plt.scatter(x, y)
    # plt.grid()
    func = np.poly1d(np.polyfit(x, y, 1))
    x.sort()
    plt.plot(x, func(x), label="Polyfit y=ax+b")
    plt.legend()
    plt.show()

    # Calculate mean squared error
    error2 = 0.0
    err = []
    for i,x_val in enumerate(x):
        error = func(x_val) - y[i]
        error2 += error*error
        err.append(error)
    mean_squared_error = error2/len(x)
    mse_msg = "y=ax+b Mean squared error = " + str(round(mean_squared_error,2))
    print(mse_msg)
 
    # Show graph
    plt.title(sd.sname[key] + " Polyfit y=ax+b Error")
    plt.xlabel("Error (Lbs)")
    plt.ylabel("Tension (Lbs)")
    plt.scatter(err, y, label=mse_msg)
    plt.legend()
    plt.show()

    # LR Data
    slr = sl.StringLr(key)
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


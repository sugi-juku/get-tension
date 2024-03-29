#!/usr/bin/env python3
# coding: utf-8

import sys
import os
from pathlib import Path
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

import string_def as sde
import string_data as sda
import string_lr as slr

if len(sys.argv) == 1:
    print("Please give target dirpath to argument.")
    print("If you want to show sample, use tmp/sample.")
    print(sys.argv[0] + " tmp/sample")
    sys.exit()

dirpath = sys.argv[1]

if os.path.exists(dirpath) == False:
    print(dirpath + " is not found.")
    sys.exit()

dir = Path(dirpath)
files = sorted(dir.glob("*.wav"))

x = []
y = []
yy = []
cnt = 0
x_max = 0
for wavfile in files:
    wavfile = str(wavfile)
    sdata = sda.StringData()
    sdata.make_data(wavfile)
    stype = sdata.get_stype()
    stglr = slr.StringLr01(stype)
    xlist = stglr.get_lrdata_xlist(sdata)
    if cnt == 0:
        dt0 = sdata.get_datetime()
    td = sdata.get_datetime() - dt0
    hours = td.total_seconds()/3600.0
    x.append(hours)
    mst = sdata.get_main_string()
    cst = sdata.get_cross_string()
    y.append(stglr.get_lrcal_tension_cor(xlist, mst, cst))
    yy.append(sdata.get_tension())
    cnt += 1
    x_max = td.seconds

# Show graph
sdef = sde.StringDef(stype)
if sdata.get_cross_string() == "":
    plt_title = sdef.get_name(sdata.get_main_string())
else:
    plt_title = sdef.get_name(sdata.get_main_string()) + " / " + sdef.get_name(sdata.get_cross_string())

plt.title(plt_title)
plt.xlabel("Time (Hours)")
plt.ylabel("Tension (lbs)")
plt.plot(x, y, label="predicted Tension")
plt.plot(x, yy, label="Machine Tension")
plt.legend()
plt.show()

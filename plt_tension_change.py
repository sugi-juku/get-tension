#!/usr/bin/env python3
# coding: utf-8

import sys
import os
from pathlib import Path
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

import string_def as sdf
import string_data as sd
import string_lr as sl

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
    sdata = sd.StringData()
    sdata.make_data(wavfile)
    stype = sdata.get_stype()
    slr = sl.StringLr00(stype)
    xlist = slr.get_lrdata_xlist(sdata)
    if cnt == 0:
        dt0 = sdata.get_datetime()
    td = sdata.get_datetime() - dt0
    hours = td.total_seconds()/3600.0
    x.append(hours)
    y.append(slr.get_lrcal_tension(xlist))
    yy.append(sdata.get_tension())
    cnt += 1
    x_max = td.seconds

# Show graph
sdef = sdf.StringDef(stype)
plt.title(sdef.get_name(sdata.get_main_string()))
plt.xlabel("Time (Hours)")
plt.ylabel("Tension (Lbs)")
plt.plot(x, y, label="predicted Tension")
plt.plot(x, yy, label="Machine Tension")
plt.legend()
plt.show()

#!/usr/bin/env python3
# coding: utf-8

import os
import sys

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

import string_rec as sr
import string_data as sd
import string_lr as sl

if len(sys.argv) == 1:
    print("Please give stringing argstr to argument.")
    sys.exit()

srec = sr.StringRec(sys.argv[1], "tmp/")
cvs_append = 1

tension = []
for filename in srec.get_file_list():
    sdata = sd.StringData()
    sdata.make_data(filename, cvs_append, "tmp.csv")
    stype = sdata.get_stype()
    slr = sl.StringLr00(stype)
    xlist = slr.get_lrdata_xlist(sdata)
    tension.append(slr.get_lrcal_tension(xlist))

total = 0.0
avg = 0.0
for i, val in enumerate(tension):
    rstr = str(i+1) + ": " + str(round(val, 2)) + " Lbs"
    print(rstr)
    total += float(val)
avg = total/len(tension)
rstr = "Average: " + str(round(avg, 2)) + " Lbs"
print(rstr)

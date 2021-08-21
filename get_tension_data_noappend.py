#!/usr/bin/env python3
# coding: utf-8

import os
import sys

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

import string_rec as sre
import string_data as sda
import string_lr as slr

if len(sys.argv) == 1:
    print("Please give stringing argstr to argument.")
    sys.exit()

srec = sre.StringRec(sys.argv[1], "tmp/")
csv_append = 1

tension = []
for filename in srec.get_file_list():
    sdata = sda.StringData()
    sdata.make_data(filename, csv_append, "tmp.csv")
    stype = sdata.get_stype()
    stglr = slr.StringLr01(stype)
    xlist = stglr.get_lrdata_xlist(sdata)
    mst = sdata.get_main_string()
    cst = sdata.get_cross_string()
    tension.append(stglr.get_lrcal_tension_cor(xlist, mst, cst))

total = 0.0
avg = 0.0
for i, val in enumerate(tension):
    rstr = str(i+1) + ": " + str(round(val, 2)) + " lbs"
    print(rstr)
    total += float(val)
avg = total/len(tension)
rstr = "Average: " + str(round(avg, 2)) + " lbs"
print(rstr)

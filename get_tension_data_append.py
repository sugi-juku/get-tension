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

srec = sr.StringRec(sys.argv[1])
csv_append = 1

tension = []
for filename in srec.get_file_list():
    sdata = sd.StringData()
    sdata.make_data(filename)
    stype = sdata.get_stype()
    slr = sl.StringLr01(stype)
    xlist = slr.get_lrdata_xlist(sdata)
    tension.append(slr.get_lrcal_tension(xlist))

tension_error = 0.0
for i, val in enumerate(tension):
    tension_error += abs(tension[0]-val)
tension_error = tension_error / (len(tension) - 1)
print("MAError = " + str(tension_error))

rstr = ""
if tension_error > sd.tension_error_val[stype]:
    for filename in srec.get_file_list():
        os.remove(filename)
        print("Removed: " + filename)
    rstr = "Measurement error.\nPlease try again."
else:
    if csv_append == 1:
        for filename in srec.get_file_list():
            sdata = sd.StringData()
            sdata.make_data(filename, csv_append)
    total = 0.0
    avg = 0.0
    for i, val in enumerate(tension):
        rstr += str(i+1) + ": " + str(round(val, 2)) + " lbs\n"
        total += float(val)
    avg = total/len(tension)
    rstr += "Average: " + str(round(avg, 2)) + " lbs"

print(rstr)

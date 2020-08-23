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

srec = sre.StringRec(sys.argv[1])
csv_append = 1

tension = []
for filename in srec.get_file_list():
    sdata = sda.StringData()
    sdata.make_data(filename)
    stype = sdata.get_stype()
    stglr = slr.StringLr01(stype)
    xlist = stglr.get_lrdata_xlist(sdata)
    tension.append(stglr.get_lrcal_tension(xlist))

tension_error = 0.0
for i, val in enumerate(tension):
    tension_error += abs(tension[0]-val)
tension_error = tension_error / (len(tension) - 1)
print("MAError = " + str(tension_error))

rstr = ""
if tension_error > sda.tension_error_val[stype]:
    for filename in srec.get_file_list():
        os.remove(filename)
        print("Removed: " + filename)
    rstr = "Measurement error.\nPlease try again."
else:
    if csv_append == 1:
        for filename in srec.get_file_list():
            sdata = sda.StringData()
            sdata.make_data(filename, csv_append)
    total = 0.0
    avg = 0.0
    for i, val in enumerate(tension):
        rstr += str(i+1) + ": " + str(round(val, 2)) + " lbs\n"
        total += float(val)
    avg = total/len(tension)
    rstr += "Average: " + str(round(avg, 2)) + " lbs"

print(rstr)

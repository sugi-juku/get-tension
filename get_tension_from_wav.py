#!/usr/bin/env python3
# coding: utf-8

import os
import sys

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

import string_data as sda
import string_lr as slr

wavfile = sys.argv[1]

if os.path.isfile(wavfile) == False:
    print(wavfile + " is not found.")
    sys.exit()

sdata = sda.StringData()
sdata.make_data(wavfile)
stype = sdata.get_stype()
stglr = slr.StringLr01(stype)
xlist = stglr.get_lrdata_xlist(sdata)
mst = sdata.get_main_string()
cst = sdata.get_cross_string()
tension = stglr.get_lrcal_tension_cor(xlist, mst, cst)
print("Tension = " + str(round(tension, 2)) + " lbs")

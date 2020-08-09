#!/usr/bin/env python3
# coding: utf-8

import os
import sys

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

import string_data as sd
import string_lr as sl

wavfile = sys.argv[1]

if os.path.isfile(wavfile) == False:
    print(wavfile + " is not found.")
    sys.exit()

sdata = sd.StringData()
sdata.make_data(wavfile)
stype = sdata.get_stype()
slr = sl.StringLr01(stype)
xlist = slr.get_lrdata_xlist(sdata)
print("Tension = " + str(round(slr.get_lrcal_tension(xlist), 2)) + " Lbs")

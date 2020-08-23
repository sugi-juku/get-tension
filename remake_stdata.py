#!/usr/bin/env python3
# coding: utf-8

import sys
import os
from pathlib import Path

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

import string_rec as sre
import string_data as sda


dirpath = sre.WAVDIR

if os.path.exists(dirpath) == False:
    print(dirpath + " is not found.")
    sys.exit()

for stype, file in sda.stdata_file.items():
    csv_file = file + ".rmk"
    if os.path.exists(csv_file) == True:
        print(csv_file + " already exists.")
        sys.exit()
    
dir = Path(dirpath)
files = sorted(dir.glob("*.wav"))

for wavfile in files:
    wavfile = str(wavfile)
    sarg = sda.StringArg(wavfile)
    sdata = sda.StringData()
    stype = sarg.get_stype()
    csv_append = 1
    csv_file = sda.stdata_file[stype] + ".rmk"
    sdata.make_data(wavfile, csv_append, csv_file)

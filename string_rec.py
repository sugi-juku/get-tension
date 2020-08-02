#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import numpy as np
import sounddevice as sdev
import soundfile as sfile
from datetime import datetime

WAVDIR = "wavdata/"

class StringRec:
    file_list = []

    def __init__(self, argstr, wavdir=WAVDIR, rec_n=2, rec_sec=2, fs=44100):
        for i in range(rec_n):
            filename = wavdir + datetime.today().strftime("%Y%m%d%H%M%S") + "_" + argstr + ".wav"
            self.file_list.append(filename)
            print(f"{i}:Recording ...")
            data = sdev.rec(int(rec_sec * fs), samplerate=fs, channels=1)
            sdev.wait()
            sfile.write(filename, data, fs)
            print(f"{i}:Saved {filename}")


    def get_file_list(self):
        return self.file_list

    def init_file_list(self):
        self.file_list = []

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

    sr = StringRec("T_40_YOPTF120_98_16-19", "tmp/")
    print(sr.get_file_list())

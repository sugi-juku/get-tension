#!/usr/bin/env python3
# coding: utf-8

import numpy as np
import sys
import os
import soundfile as sfile
# import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

import string_data as sda

class StringFft:
    # Max amplitude
    max_y=0.0
    # Fundamental frequency (f0)
    max_x=0.0
    # Index of max amplitude
    max_i=0

    def __init__(self, wavfile):
        sarg = sda.StringArg(wavfile)
        stype = sarg.get_stype()

        # Frequency Search range
        x_smin = {}
        x_smin["B"] = 1000
        x_smin["T"] = 450
        x_smax = {}
        x_smax["B"] = 1280
        x_smax["T"] = 750

        data, fs = sfile.read(wavfile)

        # If you want to plot data, import matplotlib
        # plt.plot(data)
        # plt.grid()
        # plt.show()

        fft_data = np.abs(np.fft.fft(data))
        freq_data = np.fft.fftfreq(data.shape[0], d=1.0/fs)

        # If you want to plot data, import matplotlib
        # plt.plot(freq_data, fft_data)
        # plt.xlim(0, 3000)
        # plt.show()

        self.max_y=0.0
        self.max_x=0.0
        self.max_i=0

        # Search f0
        for i,val in enumerate(freq_data):
            if x_smin[stype] <= freq_data[i] <= x_smax[stype]:
                if self.max_y < fft_data[i]:
                    self.max_y=fft_data[i]
                    self.max_x=freq_data[i]
                    self.max_i=i

        # print(max(fft_data[0:self.max_i+50]))
        # print(np.argmax(fft_data[0:self.max_i+50]))
        # print(abs(freq_data[np.argmax(fft_data[0:self.max_i+50])]))

        # print(self.max_y)
        # print(self.max_i)
        # print(self.max_x)

    def get_f0(self):
        return self.max_x

if __name__ == "__main__":
    sf = StringFft("wavdata/20200222163539_T_45_GOAKP16-YOPTF120_98_16-19.wav")
    print(sf.get_f0())
    sf = StringFft("wavdata/20200307162726_B_27_YOBG80P.wav")
    print(sf.get_f0())

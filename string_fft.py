#!/usr/bin/env python3
# coding: utf-8

import numpy as np
import sys
import os
import soundfile as sfile
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

import string_data as sda

class StringFft:
    # Max amplitude
    max_y=0.0
    # Fundamental frequency (f0)
    max_x=0.0
    # Index of max amplitude
    max_i=0

    def __init__(self, wavfile, plt_show=0):
        sarg = sda.StringArg(wavfile)
        stype = sarg.get_stype()
        tension = sarg.get_tension()

        #
        # Frequency Search range
        #
        ADD_FREQ = 125
        x_smin = {}
        x_smin["B"] = 950
        x_smin["T"] = 450
        # Polyfit coef
        pf_a = {}
        pf_a["B"] = 0.038
        pf_a["T"] = 0.067
        pf_b = {}
        pf_b["B"] = -22.5
        pf_b["T"] = 8.3
        x_smax = {}
        x_smax[stype] = (tension-pf_b[stype])/pf_a[stype]+ADD_FREQ
 
        data, fs = sfile.read(wavfile)

        if plt_show == 1:
            time = []
            for i,val in enumerate(data):
                time.append(i/fs)
            plt.plot(time, data)
            plt.show()

        fft_data = np.abs(np.fft.fft(data))
        freq_data = np.fft.fftfreq(data.shape[0], d=1.0/fs)

        if plt_show == 1:
            plt.plot(freq_data, fft_data)
            plt.xlim(0, 3000)
            plt.show()

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
    sf = StringFft("wavdata/20200307162726_B_27_YOBG80P_56.wav", plt_show=1)
    print(sf.get_f0())

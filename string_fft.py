#!/usr/bin/env python3
# coding: utf-8

import numpy as np
import sys
import os
import soundfile as sfile
import matplotlib.pyplot as plt
import scipy.signal as sig

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
        if os.path.isfile(wavfile) == False:
            print(wavfile + " is not found.")
            sys.exit()

        sarg = sda.StringArg(wavfile)
        stype = sarg.get_stype()
        tension = sarg.get_tension()

        #
        # Frequency Search range
        #
        peak_cut = 0.75
        add_freq = {}
        add_freq["B"] = 180
        add_freq["T"] = 200
        x_smin = {}
        x_smin["B"] = 950
        x_smin["T"] = 450
        # Polyfit coef
        pf_a = {}
        pf_a["B"] = 0.027
        pf_a["T"] = 0.056
        pf_b = {}
        pf_b["B"] = -10.1
        pf_b["T"] = 14.1
        x_smax = {}
        x_smax[stype] = (tension-pf_b[stype])/pf_a[stype]+add_freq[stype]

        data, fs = sfile.read(wavfile)

        if plt_show == 1:
            time = []
            for i,val in enumerate(data):
                time.append(i/fs)
            plt.plot(time, data)
            plt.show()

        fft_data = np.abs(np.fft.fft(data))
        freq_data = np.fft.fftfreq(data.shape[0], d=1.0/fs)

        peak_i = sig.argrelmax(fft_data, order=256)[0]

        self.max_y = 0.0
        self.max_x = 0.0
        self.max_i = 0

        # Search f0
        tmp_max_y = 0.0
        for i in peak_i:
            if x_smin[stype] <= freq_data[i] <= x_smax[stype]:
                if tmp_max_y < fft_data[i]:
                    tmp_max_y = fft_data[i]

        peak_cnt = 0
        for i in peak_i:
            if x_smin[stype] <= freq_data[i] <= x_smax[stype]:
                if self.max_y < fft_data[i] and tmp_max_y*peak_cut < fft_data[i]:
                    peak_cnt += 1
                    # Get first peak
                    if peak_cnt < 2:
                        self.max_y = fft_data[i]
                        self.max_x = freq_data[i]
                        self.max_i = i
                        break

        if plt_show == 1:
            plt.plot(freq_data, fft_data)
            plt.xlim(0, 3000)
            plt.vlines(x_smin[stype], 0, self.max_y, colors='red', linestyles='dashed')
            plt.vlines(x_smax[stype], 0, self.max_y, colors='red', linestyles='dashed')
            plt.hlines(tmp_max_y*peak_cut, 0, 3000, colors='blue', linestyles='dashed')
            plt.plot(freq_data[peak_i], fft_data[peak_i], 'ro')
            plt.show()

        # print(max(fft_data[0:self.max_i+50]))
        # print(np.argmax(fft_data[0:self.max_i+50]))
        # print(abs(freq_data[np.argmax(fft_data[0:self.max_i+50])]))

        # print(self.max_y)
        # print(self.max_i)
        # print(self.max_x)

    def get_f0(self):
        return self.max_x

if __name__ == "__main__":
    sf = StringFft("wavdata/20210224201248_T_46_LU4GS125_100_16-19.wav", plt_show=1)
    print(sf.get_f0())
    sf = StringFft("wavdata/20210424174617_B_27_YOBG80P_56.wav", plt_show=1)
    print(sf.get_f0())

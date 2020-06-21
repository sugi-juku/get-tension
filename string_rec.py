#!/usr/bin/env python3
# coding: utf-8

import pyaudio
import wave
import os
import numpy as np
from datetime import datetime

RATE = 44100

WAVDIR = "wavdata/"

class StringRec:
    file_list = []

    def __init__(self, argstr, wavdir=WAVDIR, rec_n=2, rec_sec=2):
        # Sound data format
        chunk = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RECORD_SECONDS = rec_sec

        threshold = 0.01

        # Start recording
        p = pyaudio.PyAudio()
        stream = p.open(format = FORMAT,
            channels = CHANNELS,
            rate = RATE,
            input = True,
            frames_per_buffer = chunk
        )

        cnt = 0

        while True:
            data = stream.read(chunk)
            x = np.frombuffer(data, dtype="int16") / 32768.0

            if x.max() > threshold:
                filename = wavdir + datetime.today().strftime("%Y%m%d%H%M%S") + "_" + argstr + ".wav"
                self.file_list.append(filename)
                print(cnt, filename)

                all = []
                all.append(data)
                for i in range(0, int(RATE / chunk * int(RECORD_SECONDS))):
                    data = stream.read(chunk)
                    all.append(data)
                data = b''.join(all)

                out = wave.open(filename,'w')
                out.setnchannels(CHANNELS)
                out.setsampwidth(2)
                out.setframerate(RATE)
                out.writeframes(data)
                out.close()

                print("Saved.")
                cnt += 1

            if cnt > rec_n-1:
                break

        stream.close()
        p.terminate()

    def get_file_list(self):
        return self.file_list

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    sr = StringRec("T_40_YOPTF120_98_16-19", "tmp/")
    print(sr.get_file_list())

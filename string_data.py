#!/usr/bin/env python3
# coding: utf-8

import csv
import datetime as dt
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

import string_fft as sf

sname = {}
sname["B"] = "Badminton"
sname["T"] = "Tennis"

stdata_file = {}
stdata_file["B"] = "stdata_b.csv"
stdata_file["T"] = "stdata_t.csv"

stdata_header = ["DateTime", "SType", "Tension", "Frequency", "MainString", "CrossString", "FaceSize", "Pattern"]


def get_argstr(stype, main_t, cross_t, main_s, cross_s, size, main_n, cross_n, dtm=""):
    if dtm == "":
        argstr = stype + "_" + main_t
    else:
        argstr = dtm + "_" + stype + "_" + main_t
    if cross_t != "":
        argstr += "-" + cross_t
    argstr += "_" + main_s
    if cross_s != "":
        argstr += "-" + cross_s
    if size != "":
        argstr += "_" + size
    if stype == "T":
        argstr += "_" + main_n + "-" + cross_n
    return argstr


class StringArg:
    arg_list = []
    tension = 0.0
    main_tension = 0.0
    cross_tension = 0.0
    stg = []
    size = ""
    patternstr = ""
    main_pat_n = 0
    cross_pat_n = 0

    def __init__(self, wavfile):
        self.set_data_from_filename(wavfile)

    def set_data_from_filename(self, wavfile):
        filename = os.path.basename(wavfile)
        data = filename.replace(".wav","")
        self.arg_list = data.split("_")

        # Tension
        ts = self.arg_list[2].split("-")
        if len(ts)==2:
            self.tension = (float(ts[0])+float(ts[1]))/2.0
            self.main_tension = float(ts[0])
            self.cross_tension = float(ts[1])
        else:
            self.tension = float(ts[0])
            self.main_tension = float(ts[0])
            self.cross_tension = float(ts[0])

        # String
        self.stg = self.arg_list[3].split("-")
        self.stg.append("")

        # FaceSize
        if len(self.arg_list) > 4:
            self.size = self.arg_list[4]

        # String Pattern
        if len(self.arg_list) > 4:
            self.patternstr = self.arg_list[5]
            pat = self.arg_list[5].split("-")
            self.main_pat_n = int(pat[0])
            self.cross_pat_n = int(pat[1])

    def get_datetimestr(self):
        return self.arg_list[0]

    def get_datetime(self):
        return dt.datetime.strptime(self.arg_list[0], "%Y%m%d%H%M%S")

    def get_stype(self):
        return self.arg_list[1]

    def get_tensionstr(self):
        return self.arg_list[2]

    def get_tension(self):
        return self.tension

    def get_main_tension(self):
        return self.main_tension

    def get_cross_tension(self):
        return self.cross_tension

    def get_stringstr(self):
        return self.arg_list[3]

    def get_main_string(self):
        return self.stg[0]

    def get_cross_string(self):
            return self.stg[1]

    def get_size(self):
        return self.size

    def get_patternstr(self):
        return self.patternstr

    def get_main_pat_n(self):
        return self.main_pat_n

    def get_cross_pat_n(self):
        return self.cross_pat_n


class StringData(StringArg):
    row_list = []

    def __init__(self, row_list=None):
        if row_list != None:
            self.set_data_from_row(row_list)

    def set_data_from_row(self, row_list):
        self.row_list = row_list

        st = row_list[2].split("-")
        st.append("")
        if row_list[1] == "T":
            pt = row_list[7].split("-")
        else:
            pt = ["", ""]

        argstr = get_argstr(row_list[1], st[0], st[1], row_list[4], row_list[5], row_list[6], pt[0], pt[1], row_list[0]) 
        self.set_data_from_filename(argstr)

    def make_data(self, wavfile, csv_append=0, csv_file=""):
        self.set_data_from_filename(wavfile)
        sfft = sf.StringFft(wavfile)
        
        self.row_list.clear()
        self.row_list.append(self.get_datetimestr())
        self.row_list.append(self.get_stype())
        self.row_list.append(self.get_tensionstr())
        self.row_list.append(sfft.get_f0())
        self.row_list.append(self.get_main_string())
        self.row_list.append(self.get_cross_string())
        self.row_list.append(self.get_size())
        self.row_list.append(self.get_patternstr())
        print(self.row_list)

        # write CSV DATA
        if csv_append == 1:
            if csv_file == "":
                csv_file = stdata_file[self.get_stype()]
            if os.path.exists(csv_file) == False:
                file_exists = False
            else:
                file_exists = True
            with open(csv_file, "a") as csvf:
                writer = csv.writer(csvf)
                if file_exists == False:
                    writer.writerow(stdata_header)
                writer.writerow(self.row_list)

    def get_f0(self):
        if len(self.row_list) > 1:
            return float(self.row_list[3])


if __name__ == "__main__":
    sarg = StringArg("wavfile/20200402181728_T_46_BABLAST125-YOPTF120_100_16-19.wav")
    print(sarg.arg_list, sarg.get_datetime(), sarg.get_patternstr())
    sarg = StringArg("20200312192739_B_20_BG65TI.wav")
    print(sarg.arg_list, sarg.get_datetime())
    print(get_argstr("T", "40", "", "GOMS16", "", "98", "16", "19", "20200426183610"))
    print(get_argstr("B", "25", "", "YOBG65TI", "", "", "", "", "20200426183610"))
    sd = StringData()
    sd.make_data("wavdata/20200222163539_T_45_GOAKP16-YOPTF120_98_16-19.wav",1,"test.csv")
    print(sd.get_f0(),sd.get_tension())


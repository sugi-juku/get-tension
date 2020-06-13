#!/usr/bin/env python
# coding: utf-8

import csv
import os
import numpy as np
from sklearn.linear_model import LinearRegression

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import string_def as sdf
import string_data as sda

class StringLr:
    stype = ""
    x = []
    y = []
    lrcal_y = []
    error = []

    lr_header = {}
    lr_header["B"] = ["Tension","F0","Gauge"]
    lr_header["T"] = ["Tension","F0","Gauge","Density","FaceSize","PatternNumber"]

    lrdata_file = {}
    lrdata_file["B"] = "lrdata_b.csv"
    lrdata_file["T"] = "lrdata_t.csv"

    lrcoef_file = {}
    lrcoef_file["B"] = "lrcoef_b.csv"
    lrcoef_file["T"] = "lrcoef_t.csv"

    def __init__(self, stype):
        self.stype = stype

    def fit(self, write_lrdata=1): 
        lr = LinearRegression()

        if write_lrdata == 1:
            # Write Header for LrData
            with open(self.lrdata_file[self.stype], "w") as csvlf:
                writer = csv.writer(csvlf)
                writer.writerow(self.lr_header[self.stype])

        self.x=[]
        self.y=[]
        with open(sda.stdata_file[self.stype]) as csvf:
            reader = csv.reader(csvf)
            header = next(reader)
            # print(header)
            for row in reader:
                sdata = sda.StringData(row)
                tmp=[]

                # Tension
                self.y.append(float(sdata.get_tension()))
                tmp.append(float(sdata.get_tension()))

                xlist = self.get_lrdata_xlist(sdata)
                self.x.append(xlist)
                tmp.extend(xlist)
                # print(tmp)

                if write_lrdata == 1:
                    # Write Data for LrData
                    with open(self.lrdata_file[self.stype], "a") as csvlf:
                        writer = csv.writer(csvlf)
                        writer.writerow(tmp)

        npa_x = np.array(self.x)
        npa_y = np.array(self.y)
        lr.fit(npa_x, npa_y)

        lr_coef = []
        for val in lr.coef_:
            lr_coef.append(val)
        lr_coef.append(lr.intercept_)

        with open(self.lrcoef_file[self.stype], "w") as csvlf:
            writer = csv.writer(csvlf)
            writer.writerow(lr_coef)

    def get_lrdata_xlist(self, sdata):
        if self.stype == "B":
            return self.get_lrdata_xlist_b(sdata)
        if self.stype == "T":
            return self.get_lrdata_xlist_t(sdata)
        
    def get_lrdata_xlist_b(self, sdata):
        sdef = sdf.StringDef(self.stype)
        xlist=[]

        # F0
        xlist.append(float(sdata.get_f0()))

        # Main String
        msg=float(sdef.get_gauge(sdata.get_main_string()))
        # Cross String
        if sdata.get_cross_string()=='':
            csg=float(sdef.get_gauge(sdata.get_main_string()))
        else:
            csg=float(sdef.get_gauge(sdata.get_cross_string()))

        # Gauge AVG
        xlist.append((msg+csg)/2.0)

        return xlist

    def get_lrdata_xlist_t(self, sdata):
        sdef = sdf.StringDef(self.stype)
        xlist=[]

        # F0
        xlist.append(float(sdata.get_f0()))

        # Main String
        msg=float(sdef.get_gauge(sdata.get_main_string()))
        msd=float(sdef.get_density(sdata.get_main_string()))
        # Cross String
        if sdata.get_cross_string()=='':
            csg=float(sdef.get_gauge(sdata.get_main_string()))
            csd=float(sdef.get_density(sdata.get_main_string()))
        else:
            csg=float(sdef.get_gauge(sdata.get_cross_string()))
            csd=float(sdef.get_density(sdata.get_cross_string()))

        # Gauge AVG
        xlist.append((msg+csg)/2.0)
        # Density AVG
        xlist.append((msd+csd)/2.0)
        # Face Size
        xlist.append(float(sdata.get_size()))
        # Pattern Number
        xlist.append(sdata.get_main_pat_n()+sdata.get_cross_pat_n())
        return xlist

    def get_lrcal_tension(self, xlist):
        tension = 0.0
        if self.stype == "B":
            tension = self.get_lrcal_tension_b(xlist)
        if self.stype == "T":
            tension = self.get_lrcal_tension_t(xlist)
        return tension
    
    def get_lrcal_tension_b(self, xlist):
        f0 = xlist[0]
        gauge = xlist[1]
        with open(self.lrcoef_file[self.stype]) as csvf:
            reader = csv.reader(csvf, quoting=csv.QUOTE_NONNUMERIC)
            coef = next(reader)
            # print coef
            tension = 0
            tension = coef[0]*float(f0)+coef[1]*float(gauge)+coef[2]
            return tension

    def get_lrcal_tension_t(self, xlist):
        f0 = xlist[0]
        gauge = xlist[1]
        density = xlist[2]
        size = xlist[3]
        pat_n = xlist[4]
        with open(self.lrcoef_file[self.stype]) as csvf:
            reader = csv.reader(csvf, quoting=csv.QUOTE_NONNUMERIC)
            coef = next(reader)
            # print coef
            tension = 0
            tension = coef[0]*float(f0)+coef[1]*float(gauge)+coef[2]*float(density)+coef[3]*float(size)+coef[4]*float(pat_n)+coef[5]
            return tension

    def get_mean_squared_error(self):
        if len(self.x) == 0:
            return 0.0
        else:
            sum_error2 = 0.0
            self.lrcal_y = []
            self.error = []
            for i,xlist in enumerate(self.x):
                self.lrcal_y.append(self.get_lrcal_tension(xlist))
                error = self.lrcal_y[i] - self.y[i]
                self.error.append(error)
                sum_error2 += error*error
            return sum_error2/len(self.x)
            
            
if __name__ == "__main__":
    slr = StringLr("B")
    slr.fit()
    print("Badminton")
    print("Mean squared error = " + str(slr.get_mean_squared_error()))

    slr = StringLr("T")
    slr.fit()
    print("Tennis")
    print("Mean squared error = " + str(slr.get_mean_squared_error()))

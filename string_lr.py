#!/usr/bin/env python3
# coding: utf-8

import csv
import os
import sys
import numpy as np
from sklearn.linear_model import LinearRegression

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

import string_def as sdf
import string_data as sda

class StringLr:
    stype = ""
    x = []
    y = []
    lrcal_y = []
    error = []

    # Mean Absolute Error
    maerror = 0.0
    # Mean Squared Error
    mserror = 0.0
    # R2 Score
    r2_score = 0.0

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

        self.x.clear()
        self.y.clear()
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

        # Caluculate MAE, MSE, R2
        sum_error = 0.0
        sum_error2 = 0.0
        sum_error2_avg = 0.0
        self.lrcal_y.clear()
        self.error.clear()
        y_avg = sum(self.y)/len(self.y)
        for i,xlist in enumerate(self.x):
            self.lrcal_y.append(self.get_lrcal_tension(xlist))
            error = self.y[i]-self.lrcal_y[i]
            error_avg = self.y[i]-y_avg
            self.error.append(error)
            sum_error += abs(error)
            sum_error2 += error*error
            sum_error2_avg += error_avg*error_avg
            self.maerror = sum_error/len(self.x)
            self.mserror = sum_error2/len(self.x)
            self.r2_score = 1-sum_error2/sum_error2_avg

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
            tension = 0.0
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
            tension = 0.0
            tension = coef[0]*float(f0)+coef[1]*float(gauge)+coef[2]*float(density)+coef[3]*float(size)+coef[4]*float(pat_n)+coef[5]
            return tension

    def get_mean_squared_error(self):
        return self.mserror

    def get_mean_absolute_error(self):
        return self.maerror

    def get_r2_score(self):
        return self.r2_score


class StringLr00(StringLr):
    lrdata_file = {}
    lrdata_file["B"] = "lrdata00_b.csv"
    lrdata_file["T"] = "lrdata00_t.csv"

    lrcoef_file = {}
    lrcoef_file["B"] = "lrcoef00_b.csv"
    lrcoef_file["T"] = "lrcoef00_t.csv"

    lr_header = {}
    lr_header["B"] = ["Tension","F0","MainGauge","CrossGauge"]
    lr_header["T"] = ["Tension","F0","MainGauge","MainDensity","CrossGauge","CrossDensity","FaceSize","MainPatN","CrossPatN"]
    
    def __init__(self, stype):
        super().__init__(stype)

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

        # Main Gaug
        xlist.append(msg)
        # Main Density
        xlist.append(msd)
        # Cross Gauge
        xlist.append(csg)
        # Cross Density
        xlist.append(csd)
        # Face Size
        xlist.append(float(sdata.get_size()))
        # Main Pattern Number
        xlist.append(sdata.get_main_pat_n())
        # Cross Pattern Number
        xlist.append(sdata.get_cross_pat_n())
        return xlist

    def get_lrcal_tension_t(self, xlist):
        f0 = xlist[0]
        msg = xlist[1]
        msd = xlist[2]
        csg = xlist[3]
        csd = xlist[4]
        size = xlist[5]
        mpat_n = xlist[6]
        cpat_n = xlist[7]
        with open(self.lrcoef_file[self.stype]) as csvf:
            reader = csv.reader(csvf, quoting=csv.QUOTE_NONNUMERIC)
            coef = next(reader)
            # print coef
            tension = 0.0
            tension = coef[0]*float(f0)+coef[1]*float(msg)+coef[2]*float(msd)+coef[3]*float(csg)+coef[4]*float(csd)+coef[5]*float(size)+coef[6]*float(mpat_n)+coef[7]*float(cpat_n)+coef[8]
            return tension

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

        # Main Gauge
        xlist.append(msg)
        # Cross Gauge
        xlist.append(csg)

        return xlist

    def get_lrcal_tension_b(self, xlist):
        f0 = xlist[0]
        msg = xlist[1]
        csg = xlist[2]
        with open(self.lrcoef_file[self.stype]) as csvf:
            reader = csv.reader(csvf, quoting=csv.QUOTE_NONNUMERIC)
            coef = next(reader)
            # print coef
            tension = 0.0
            tension = coef[0]*float(f0)+coef[1]*float(msg)+coef[2]*float(csg)+coef[3]
            return tension


class StringLr01(StringLr00):
    lrdata_file = {}
    lrdata_file["B"] = "lrdata01_b.csv"
    lrdata_file["T"] = "lrdata01_t.csv"

    lrcoef_file = {}
    lrcoef_file["B"] = "lrcoef01_b.csv"
    lrcoef_file["T"] = "lrcoef01_t.csv"

    lr_header = {}
    lr_header["B"] = ["Tension","F0","MainGauge","CrossGauge"]
    lr_header["T"] = ["Tension","F0","MainGauge","MainDensity","CrossGauge","CrossDensity","FaceSize","MainPatN","CrossPatN","MainYoung","CrossYoung"]
    
    # Young's Modulous (kg/mm2)
    # 65(6), 411-416(1996), J.Seric.Sci.Jpn. Mechanical Properties of Silk String.
    young_mod = {}
    young_mod["N"] = 400
    young_mod["P"] = 1000
    young_mod["G"] = 450

    def __init__(self, stype):
        super().__init__(stype)

    def get_lrdata_xlist_t(self, sdata):
        sdef = sdf.StringDef(self.stype)
        xlist=[]

        # F0
        xlist.append(float(sdata.get_f0()))

        # Main String
        msg=float(sdef.get_gauge(sdata.get_main_string()))
        msd=float(sdef.get_density(sdata.get_main_string()))
        msm=sdef.get_material(sdata.get_main_string())
        # Cross String
        if sdata.get_cross_string()=='':
            csg=float(sdef.get_gauge(sdata.get_main_string()))
            csd=float(sdef.get_density(sdata.get_main_string()))
            csm=sdef.get_material(sdata.get_main_string())
        else:
            csg=float(sdef.get_gauge(sdata.get_cross_string()))
            csd=float(sdef.get_density(sdata.get_cross_string()))
            csm=sdef.get_material(sdata.get_cross_string())

        # Main Gaug
        xlist.append(msg)
        # Main Density
        xlist.append(msd)
        # Cross Gauge
        xlist.append(csg)
        # Cross Density
        xlist.append(csd)
        # Face Size
        xlist.append(float(sdata.get_size()))
        # Main Pattern Number
        xlist.append(sdata.get_main_pat_n())
        # Cross Pattern Number
        xlist.append(sdata.get_cross_pat_n())
        # Main Young's modulouns
        xlist.append(self.young_mod[msm])
        # Cross Young's modulous
        xlist.append(self.young_mod[csm])
        return xlist

    def get_lrcal_tension_t(self, xlist):
        f0 = xlist[0]
        msg = xlist[1]
        msd = xlist[2]
        csg = xlist[3]
        csd = xlist[4]
        size = xlist[5]
        mpat_n = xlist[6]
        cpat_n = xlist[7]
        msm = xlist[8]
        csm = xlist[9]
        with open(self.lrcoef_file[self.stype]) as csvf:
            reader = csv.reader(csvf, quoting=csv.QUOTE_NONNUMERIC)
            coef = next(reader)
            # print coef
            tension = 0.0
            tension = coef[0]*float(f0)+coef[1]*float(msg)+coef[2]*float(msd)+coef[3]*float(csg)+coef[4]*float(csd)+coef[5]*float(size)+coef[6]*float(mpat_n)+coef[7]*float(cpat_n)+coef[8]*float(msm)+coef[9]*float(csm)+coef[10]
            return tension


if __name__ == "__main__":
    slr = StringLr("B")
    slr.fit(write_lrdata=0)
    print("Badminton")
    print("Mean absolute error = " + str(slr.get_mean_absolute_error()))
    print("Mean squared error = " + str(slr.get_mean_squared_error()))
    print("Coefficient of determination = " + str(slr.get_r2_score()))

    slr = StringLr("T")
    slr.fit(write_lrdata=0)
    print("Tennis")
    print("Mean absolute error = " + str(slr.get_mean_absolute_error()))
    print("Mean squared error = " + str(slr.get_mean_squared_error()))
    print("Coefficient of determination = " + str(slr.get_r2_score()))

    slr = StringLr00("B")
    slr.fit(write_lrdata=0)
    print("Badminton00")
    print("Mean absolute error = " + str(slr.get_mean_absolute_error()))
    print("Mean squared error = " + str(slr.get_mean_squared_error()))
    print("Coefficient of determination = " + str(slr.get_r2_score()))

    slr = StringLr00("T")
    slr.fit(write_lrdata=0)
    print("Tennis00")
    print("Mean absolute error = " + str(slr.get_mean_absolute_error()))
    print("Mean squared error = " + str(slr.get_mean_squared_error()))
    print("Coefficient of determination = " + str(slr.get_r2_score()))

    slr = StringLr01("B")
    slr.fit(write_lrdata=0)
    print("Badminton01")
    print("Mean absolute error = " + str(slr.get_mean_absolute_error()))
    print("Mean squared error = " + str(slr.get_mean_squared_error()))
    print("Coefficient of determination = " + str(slr.get_r2_score()))

    slr = StringLr01("T")
    slr.fit(write_lrdata=1)
    print("Tennis01")
    print("Mean absolute error = " + str(slr.get_mean_absolute_error()))
    print("Mean squared error = " + str(slr.get_mean_squared_error()))
    print("Coefficient of determination = " + str(slr.get_r2_score()))

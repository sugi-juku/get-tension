#!/usr/bin/env python3
# coding: utf-8

import csv
import datetime as dt
import os
import sys
import math


class StringDef:
    """Definition of String Data

    sdef[Code] = [Name, Material('N'or'P'or'G'), Gauge, Factor]
    """

    sdef = {}
    key_list = []
    name_list = []

    deffile = {}
    deffile["T"] = "string_def_t.csv"
    deffile["B"] = "string_def_b.csv"

    matstr = {}
    matstr["N"] = "Nylon mono "
    matstr["M"] = "Nylon multi "
    matstr["P"] = "Polyester "
    matstr["G"] = "Natural "

    PI = math.pi

    def __init__(self, stype='T'):
        """
        Parameters
        ----------
        stype : str
            Sports type
            stype = 'B' or 'T'
            B: Badminton
            T: Tennis
        """

        if os.path.isfile(self.deffile[stype]) == False:
            print(self.deffile[stype] + " is not found.")
            sys.exit()

        self.sdef.clear()
        cnt = {}
        fac = {}
        with open(self.deffile[stype]) as csvf:
            reader = csv.reader(csvf)
            header = next(reader)
            # print(header)
            for row in reader:
                # Set CSV Data
                self.sdef[row[0]] = [row[1],row[2],float(row[3]),float(row[4])]
                
                # For AVG of String Material and Gauge
                gauge = row[3].replace('.','')
                key = 'ZZ' + row[2] + gauge
                self.sdef[key] = [self.matstr[row[2]]+gauge,row[2],float(row[3]),float(row[4])]
                cnt.setdefault(key, 0)
                fac.setdefault(key, 0.0)
                cnt[key] += 1
                fac[key] += float(row[4])

        # Calculate AVG of Density about Material
        if stype == "T":
            cnt_den = {}
            den = {}
            for key,val in fac.items():
                fac_avg = val/float(cnt[key])
                mat = self.get_material(key)
                gauge = self.get_gauge(key)
                cnt_den.setdefault(mat, 0)
                den.setdefault(mat, 0.0)
                cnt_den[mat] += 1
                den[mat] += self.get_density_from_factor(fac_avg, gauge)

            den_avg = {}
            for mat,val in den.items():
                den_avg[mat] = val/float(cnt_den[mat])

            for key,val in fac.items():
                mat = self.get_material(key)
                gauge = self.get_gauge(key)
                self.sdef[key][3] = self.get_factor_from_density(den_avg[mat], gauge)

        # Make sorted list
        self.key_list.clear()
        self.name_list.clear()
        for key, val in sorted(self.sdef.items()):
            self.key_list.append(key)
            self.name_list.append(val[0])

    def get_dict(self):
        return self.sdef

    def get_key_list(self):
        return self.key_list

    def get_key_from_name(self, name):
        if name == "":
            return ""
        else:
            i = self.name_list.index(name)
            return self.key_list[i]

    def get_name_list(self):
        return self.name_list

    def get_name(self, key):
        return self.sdef[key][0]

    def get_material(self, key):
        return self.sdef[key][1]

    def get_gauge(self, key):
        return self.sdef[key][2]

    def get_factor(self, key):
        return self.sdef[key][3]

    def get_factor_from_density(self, density, gauge):
        r = float(gauge)*0.1/2.0
        v = self.PI*r*r*100.0
        factor = float(density)*v
        return factor

    def get_density_from_factor(self, factor, gauge):
        r = float(gauge)*0.1/2.0
        v = self.PI*r*r*100.0
        m = float(factor)
        density = m/v
        return density

    def get_density(self, key):
        density = self.get_density_from_factor(self.get_factor(key), self.get_gauge(key))
        return density

    def get_face_density(self, key, face=98, pat_type="main", pat_n=16):
        inch = 2.54
        sample_main_max = 34.0
        sample_cross_max = 26.0
        rate = sample_cross_max/sample_main_max
        face_cm2 = inch*inch*float(face)
        main_len = math.sqrt(face_cm2/rate)
        cross_len = main_len*rate
        fact_cm = float(self.sdef[key][3])*0.01
        if pat_type == "main":
            len = main_len
        else:
            len = cross_len
        m = fact_cm*len*float(pat_n)
        h = float(self.sdef[key][2])*0.1
        v = face_cm2*h
        d = m/v
        # print(face_cm2, main_len, cross_len, len, fact_cm, m, h, v, d)
        return d


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

    sd = StringDef('T')
    # density = 1.22529565296734
    # density = 1.226522617952606
    # density = 1.368248865886832
    density = 1.2386074291183662
    print(sd.get_key_from_name("GOSEN AK PRO 16"))
    for key, val in sorted(sd.get_dict().items()):
        print(key, val, sd.get_density(key), sd.get_face_density(key, 98, "main", 16), sd.get_factor_from_density(density, sd.get_gauge(key)))
    sd = StringDef('B')
    density = 1.226522617952606
    for key, val in sorted(sd.get_dict().items()):
        print(key, val, sd.get_factor_from_density(density, sd.get_gauge(key)))


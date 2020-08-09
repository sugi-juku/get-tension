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
import string_lr as sl


slr = sl.StringLr01("B")
slr.fit()
print("Badminton")
print("Mean squared error = " + str(slr.get_mean_squared_error()))

slr = sl.StringLr01("T")
slr.fit()
print("Tennis")
print("Mean squared error = " + str(slr.get_mean_squared_error()))

#!/usr/bin/env python3
# coding: utf-8

import os
import sys

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

import string_lr as slr


stglr = slr.StringLr01("B")
stglr.fit()
print("Badminton")
print("Mean squared error = " + str(stglr.get_mean_squared_error()))

stglr = slr.StringLr01("T")
stglr.fit()
print("Tennis")
print("Mean squared error = " + str(stglr.get_mean_squared_error()))

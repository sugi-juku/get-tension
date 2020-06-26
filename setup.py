# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('get_tension_app.py', base=base)
]

setup(name='get_tension',
    version='1.1',
    description='You can get racket string tension.',
    executables=executables
    )

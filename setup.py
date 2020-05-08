# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
includefiles = ['README.txt', 'icon.ico', 'example_input.u11']
includes = []
excludes = []
packages = ["idna",
            "os",
            "matplotlib",
            "matplotlib.pyplot",
            "tkinter",
            "tkinter.filedialog",
            "win32api",
            "PIL",
            "ctypes",
            "re",
            "matplotlib.ticker"]
# Dependencies are automatically detected, but it might need
# fine tuning.


executables = [
    Executable('OrigenDA.py', base=base)
]

setup(name='OrigenDataAnalysis',
      version='1.3.0',
      description='Process data from Origen22',
      options={'build_exe': {'includes': includes, 'excludes': excludes, 'packages': packages, 'include_files': includefiles}},
      executables=executables)

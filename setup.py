# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = ["idna",
                                "os",
                                "matplotlib",
                                "matplotlib.pyplot",
                                "tkinter",
                                "tkinter.filedialog",
                                "win32api"], excludes = [])


executables = [
    Executable('main.py', base=base)
]

setup(name='Origen Data Analysis',
      version = '1.0',
      description = '',
      options = dict(build_exe = buildOptions),
      executables = executables)

import sys
from cx_Freeze import setup, Executable

#
# cx_Freeze script
# to freeze Maze of Kindred
# into a Windows executable
#

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"], "include_files": ("assets")}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Maze of Kindred",
        version = "0.1",
        description = "",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])
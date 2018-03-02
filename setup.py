from cx_Freeze import setup, Executable
import os
os.environ['TCL_LIBRARY'] = r'C:\Users\pashk\AppData\Local\Programs\Python\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\pashk\AppData\Local\Programs\Python\Python36\tcl\tk8.6'

setup(
    name = 'Checkers AI',
    version = '1.0',
    description = 'Checkers',
    executables = [Executable('gui.py')]
)

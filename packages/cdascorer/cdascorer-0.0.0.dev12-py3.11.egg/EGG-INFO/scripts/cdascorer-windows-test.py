#!/Library/Frameworks/Python.framework/Versions/3.11/bin/python3
'''
cdascorer-test

Runs cdascorer-run with the test flag -t

Output found in the file "test_cdata.csv"

'''

import subprocess
from sys import platform

if platform == "win32":
    subprocess.run(["cdascorer-windows.py", "-f", "test_cdata.csv", "-t", "True"], shell=True)
else:
    subprocess.run(["cdascorer-windows.py", "-f", "test_cdata.csv", "-t", "True"])


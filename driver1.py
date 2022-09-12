#
# Title: driver1.py
# Description: application driver
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import math
import station

if __name__ == "__main__":
    print("main")

    sr = station.StationReader()
    results = sr.reader("stations.dat")
    print(results)
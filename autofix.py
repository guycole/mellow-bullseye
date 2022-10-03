#
# Title: autofix.py
# Description: process all artifacts
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#

import station

if __name__ == "__main__":
    print("autofix start")

    sm = station.StationManager()
    sm.read_stations("stations.dat")

    print("autofix end")

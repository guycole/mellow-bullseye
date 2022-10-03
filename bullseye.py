#
# Title: bullseye.py
# Description: bullseye main
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import sys

import artifact
import map_wrapper
import station

if __name__ == "__main__":
    print("main")

    sm = station.StationManager()
    sm.read_stations("stations.dat")

    mw = map_wrapper.MapWrapper(sm)

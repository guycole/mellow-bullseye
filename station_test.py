#
# Title: station_test.py
# Description: test for station classes
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import pytest

import station


def test_station_manager():
    sm = station.StationManager()
    sm.read_stations("stations.dat")

    assert len(sm.stations) == 7

    candidate = sm.get_station("sea")
    assert candidate.equipment == "frd10"
    assert candidate.location.lat.rad_val == 0.8281567927558396
    assert candidate.location.lng.rad_val == -2.134743240068365

#
# Title: utility_test.py
# Description: tests for helper class and methods
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import math
import pytest

import utility


def test_latitude():
    lat1 = utility.Latitude(math.pi / 8.0, True)
    lat2 = utility.Latitude(-math.pi / 8.0, True)

    lat3 = utility.Latitude(math.pi / 4.0, True)
    assert str(lat3) == "45.0"
    assert lat3.dd_value == 45.0
    assert lat3.radian_value == 0.7853981633974483

    lat4 = utility.DdAngle(math.pi / 4.0, True)
    assert lat3 == lat4

    assert lat3 != lat1
    assert lat3 != lat2

    ###

    lat5 = utility.Latitude(-math.pi / 4.0, True)
    assert str(lat5) == "-45.0"
    assert lat5.dd_value == -45.0
    assert lat5.radian_value == -0.7853981633974483

    lat6 = utility.Latitude(-math.pi / 4.0, True)
    assert lat5 == lat6

    assert lat5 != lat1
    assert lat5 != lat2

    ###

    with pytest.raises(ValueError):
        lat7 = utility.Latitude(1 + math.pi / 2.0, True)


def test_longitude():
    lng1 = utility.Longitude(math.pi / 8.0, True)
    lng2 = utility.Longitude(-math.pi / 8.0, True)

    lng3 = utility.Longitude(math.pi / 4.0, True)
    assert str(lng3) == "45.0"
    assert lng3.dd_value == 45.0
    assert lng3.radian_value == 0.7853981633974483

    lng4 = utility.Longitude(math.pi / 4.0, True)
    assert lng3 == lng4

    assert lng3 != lng1
    assert lng3 != lng2

    ###

    lng5 = utility.Longitude(-math.pi / 4.0, True)
    assert str(lng5) == "-45.0"
    assert lng5.dd_value == -45.0
    assert lng5.radian_value == -0.7853981633974483

    lng6 = utility.Longitude(-math.pi / 4.0, True)
    assert lng5 == lng6

    assert lng5 != lng1
    assert lng5 != lng2

    ###

    with pytest.raises(ValueError):
        lng7 = utility.Latitude(1 + math.pi, True)


def test_location():
    lat1 = utility.Latitude(math.pi / 8.0, True)
    lng1 = utility.Longitude(math.pi / 8.0, True)
    loc1 = utility.Location(lat1, lng1)

    lat2 = utility.Latitude(-math.pi / 4.0, True)
    lng2 = utility.Longitude(-math.pi / 4.0, True)
    loc2 = utility.Location(lat2, lng2)

    lat3 = utility.Latitude(math.pi / 8.0, True)
    lng3 = utility.Longitude(math.pi / 8.0, True)
    loc3 = utility.Location(lat3, lng3)

    assert loc1 == loc3
    assert loc1 != loc2
    assert loc3 != loc2

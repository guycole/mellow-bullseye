#
# Title: utility_test.py
# Description: tests for helper class and methods
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import math
import pytest

import utility


def test_dd_equals():
    """decimal degree test"""

    # same value
    dd1 = utility.DdAngle(math.pi / 8.0, True)
    dd2 = utility.DdAngle(math.pi / 8.0, True)
    assert dd1 == dd2

    dd1 = utility.DdAngle(-math.pi / 8.0, True)
    dd2 = utility.DdAngle(-math.pi / 8.0, True)
    assert dd1 == dd2

    # within epsilon (two positive values)
    dd1 = utility.DdAngle(math.pi / 8.0, True)
    finagle = 3 * utility.EPSILON / 4.0
    dd2 = utility.DdAngle((math.pi / 8.0) + finagle, True)
    assert dd1 == dd2
    dd2 = utility.DdAngle((math.pi / 8.0) - finagle, True)
    assert dd1 == dd2

    # test bigger than epsilon (two positive values)
    dd1 = utility.DdAngle(math.pi / 8.0, True)
    finagle = 5 * utility.EPSILON / 4.0
    dd2 = utility.DdAngle((math.pi / 8.0) + finagle, True)
    assert dd1 != dd2
    dd2 = utility.DdAngle((math.pi / 8.0) - finagle, True)
    assert dd1 != dd2

    # test within epsilon (two negative values)
    dd1 = utility.DdAngle(-math.pi / 8.0, True)
    finagle = -3 * utility.EPSILON / 4.0
    dd2 = utility.DdAngle((-math.pi / 8.0) + finagle, True)
    assert dd1 == dd2
    dd2 = utility.DdAngle((-math.pi / 8.0) - finagle, True)
    assert dd1 == dd2

    # test bigger than epsilon (two negative values)
    dd1 = utility.DdAngle(-math.pi / 8.0, True)
    finagle = -5 * utility.EPSILON / 4.0
    dd2 = utility.DdAngle((-math.pi / 8.0) + finagle, True)
    assert dd1 != dd2
    dd2 = utility.DdAngle((-math.pi / 8.0) - finagle, True)
    assert dd1 != dd2

    # test within epsilon (mixed sign)
    dd1 = utility.DdAngle(utility.EPSILON / 10.0, True)
    dd2 = utility.DdAngle(-utility.EPSILON / 10.0, True)
    assert dd1 == dd2

    # test bigger than epsilon (mixed sign)
    dd1 = utility.DdAngle(math.pi / 8.0, True)
    dd2 = utility.DdAngle(-math.pi / 8.0, True)
    assert dd1 != dd2


def test_latitude():
    """latitude container test"""

    with pytest.raises(ValueError):
        utility.Latitude(1 + math.pi / 2.0, True)


def test_longitude():
    """longitude container test"""

    with pytest.raises(ValueError):
        utility.Latitude(1 + math.pi, True)


def test_location():
    """location container test"""

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

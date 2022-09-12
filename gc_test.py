
# Title: gc_test.py
# Description: test for GreatCircle
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import math
import pytest

import gcircle
import utility

def test_gcrab():
    source_lat = utility.DdAngle(0.0, False)
    source_lng = utility.DdAngle(0.0, False)
    source_loc = utility.Location(source_lat, source_lng)

    dest_lat = utility.DdAngle(10.0, False)
    dest_lng = utility.DdAngle(10.0, False)
    dest_loc = utility.Location(dest_lat, dest_lng)

    gc = gcircle.GreatCircle()
    (range, bearing) = gc.gcrab(source_loc, dest_loc)
    print(f"{range} {bearing}")
    print(f"{range*3963.3} {bearing*180.0/math.pi}")
    assert False

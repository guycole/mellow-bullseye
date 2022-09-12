#
# Title: dd_test.py
# Description: test for DdAngle
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import math
import pytest

import utility


def test_dd():
    dd0 = utility.DdAngle(1.1, False)
    dd1 = utility.DdAngle(-1.1, False)

    dd2 = utility.DdAngle(math.pi / 4.0, True)
    assert str(dd2) == "45.0"

    assert dd2.dd_value == 45.0
    assert dd2.radian_value == 0.7853981633974483

    dd3 = utility.DdAngle(math.pi / 4.0, True)
    assert dd2 == dd3

    assert dd2 != dd0
    assert dd2 != dd1

    ###

    dd4 = utility.DdAngle(-math.pi / 4.0, True)
    assert str(dd4) == "-45.0"

    assert dd4.dd_value == -45.0
    assert dd4.radian_value == -0.7853981633974483

    dd5 = utility.DdAngle(-math.pi / 4.0, True)
    assert dd4 == dd5

    assert dd4 != dd0
    assert dd4 != dd1

#
# Title: dms_test.py
# Description: test for DmsAngle
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import pytest

import utility


def test_dms():
    dms0 = utility.DmsAngle(1, 2, 3)
    dms1 = utility.DmsAngle(-1, 2, 3)

    dms2 = utility.DmsAngle(40, 51, 59)
    assert str(dms2) == "40-51-59"
    assert dms2.dms_converted == 40.866389

    dms3 = utility.DmsAngle(40, 51, 59)
    assert dms2 == dms3

    assert dms2 != dms0
    assert dms2 != dms1

    ###

    dms4 = utility.DmsAngle(124, 4, 58)
    assert str(dms4) == "124-4-58"
    assert dms4.dms_converted == 124.082778

    dms5 = utility.DmsAngle(124, 4, 58)
    assert dms4 == dms5

    assert dms4 != dms0
    assert dms4 != dms1

#
# Title: gcircle_test.py
# Description: great circle tests
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import math
import pytest

import gcircle
import utility


def test_si_wh():
    skaggs_lat = utility.Latitude(38.1793681, False)
    skaggs_lng = utility.Longitude(-122.3731450, False)
    skaggs_loc = utility.Location(skaggs_lat, skaggs_lng)

    wh_lat = utility.Latitude(44.401111, False)
    wh_lng = utility.Longitude(-67.991111, False)
    wh_loc = utility.Location(wh_lat, wh_lng)

    gc = gcircle.GreatCircle()

    # skaggs island to winter harbor
    (azimuth, distance1) = gc.gcdaz(skaggs_loc, wh_loc)
    assert azimuth.rad_val == pytest.approx(1.103833696879552, utility.EPSILON)
    assert distance1.rad_val == pytest.approx(0.7081533619986511, utility.EPSILON)

    temp_loc = gc.dazgc(skaggs_loc, azimuth, distance1)
    assert temp_loc == wh_loc

    # winter harbor to skaggs island
    (azimuth, distance2) = gc.gcdaz(wh_loc, skaggs_loc)
    assert azimuth.rad_val == pytest.approx(4.900004198967812, utility.EPSILON)
    assert distance2.rad_val == pytest.approx(distance1.rad_val, utility.EPSILON)

    temp_loc = gc.dazgc(wh_loc, azimuth, distance2)
    assert temp_loc == skaggs_loc


def test_long0():
    augsburg_lat = utility.Latitude(48.45, False)
    augsburg_lng = utility.Longitude(10.863611, False)
    augsburg_loc = utility.Location(augsburg_lat, augsburg_lng)

    wh_lat = utility.Latitude(44.401111, False)
    wh_lng = utility.Longitude(-67.991111, False)
    wh_loc = utility.Location(wh_lat, wh_lng)

    gc = gcircle.GreatCircle()

    # winter harbor to augsburg
    (azimuth, distance1) = gc.gcdaz(wh_loc, augsburg_loc)
    assert azimuth.rad_val == pytest.approx(0.9710389465471333, utility.EPSILON)
    assert distance1.rad_val == pytest.approx(0.9081281026712691, utility.EPSILON)

    temp_loc = gc.dazgc(wh_loc, azimuth, distance1)
    assert temp_loc == augsburg_loc

    # augsburg to winter harbor
    (azimuth, distance2) = gc.gcdaz(augsburg_loc, wh_loc)
    assert azimuth.rad_val == pytest.approx(5.187645334923327, utility.EPSILON)
    assert distance2.rad_val == pytest.approx(distance1.rad_val, utility.EPSILON)

    temp_loc = gc.dazgc(augsburg_loc, azimuth, distance2)
    assert temp_loc == wh_loc


def test_long180():
    wahiawa_lat = utility.Latitude(21.522222, False)
    wahiawa_lng = utility.Longitude(-158.011389, False)
    wahiawa_loc = utility.Location(wahiawa_lat, wahiawa_lng)

    finegayan_lat = utility.Latitude(13.593611, False)
    finegayan_lng = utility.Longitude(144.8525, False)
    finegayan_loc = utility.Location(finegayan_lat, finegayan_lng)

    gc = gcircle.GreatCircle()

    # wahiawa to finegayan
    (azimuth, distance1) = gc.gcdaz(wahiawa_loc, finegayan_loc)
    assert azimuth.rad_val == pytest.approx(4.74318012298315, utility.EPSILON)
    assert distance1.rad_val == pytest.approx(0.9558762231057704, utility.EPSILON)

    temp_loc = gc.dazgc(wahiawa_loc, azimuth, distance1)
    assert temp_loc == finegayan_loc

    # finegayan to wahiawa
    (azimuth, distance2) = gc.gcdaz(finegayan_loc, wahiawa_loc)
    assert azimuth.rad_val == pytest.approx(1.2752128093668078, utility.EPSILON)
    assert distance2.rad_val == pytest.approx(distance1.rad_val, utility.EPSILON)

    temp_loc = gc.dazgc(finegayan_loc, azimuth, distance2)
    assert temp_loc == wahiawa_loc


def test_north_pole():
    adak_lat = utility.Latitude(51.9425, False)
    adak_lng = utility.Longitude(-176.600556, False)
    adak_loc = utility.Location(adak_lat, adak_lng)

    edzell_lat = utility.Latitude(56.809167, False)
    edzell_lng = utility.Longitude(-2.605556, False)
    edzell_loc = utility.Location(edzell_lat, edzell_lng)

    gc = gcircle.GreatCircle()

    # adak to edzell
    (azimuth, distance1) = gc.gcdaz(adak_loc, edzell_loc)
    assert azimuth.rad_val == pytest.approx(0.06055698411302806, utility.EPSILON)
    assert distance1.rad_val == pytest.approx(1.241561805890704, utility.EPSILON)

    temp_loc = gc.dazgc(adak_loc, azimuth, distance1)
    assert temp_loc == edzell_loc

    # edzell to adak
    (azimuth, distance2) = gc.gcdaz(edzell_loc, adak_loc)
    assert azimuth.rad_val == pytest.approx(6.214981799746803, utility.EPSILON)
    assert distance2.rad_val == pytest.approx(distance1.rad_val, utility.EPSILON)

    temp_loc = gc.dazgc(edzell_loc, azimuth, distance2)
    assert temp_loc == adak_loc

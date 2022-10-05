#
# Title: gcircle_test.py
# Description: great circle tests
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import pytest

import gcircle as gc
import utility as util


def test_si_wh():
    """test great circle between Skaggs Island and Winter Harbor"""
    skaggs_lat = util.Latitude(38.1793681, False)
    skaggs_lng = util.Longitude(-122.3731450, False)
    skaggs_loc = util.Location(skaggs_lat, skaggs_lng)

    wh_lat = util.Latitude(44.401111, False)
    wh_lng = util.Longitude(-67.991111, False)
    wh_loc = util.Location(wh_lat, wh_lng)

    # skaggs island to winter harbor
    (azimuth, distance1) = gc.GreatCircle.gcdaz(skaggs_loc, wh_loc)
    assert azimuth.rad_val == pytest.approx(1.103833696879552, util.EPSILON)
    assert distance1.rad_val == pytest.approx(0.7081533619986511, util.EPSILON)

    temp_loc = gc.GreatCircle.dazgc(skaggs_loc, azimuth, distance1)
    assert temp_loc == wh_loc

    # winter harbor to skaggs island
    (azimuth, distance2) = gc.GreatCircle.gcdaz(wh_loc, skaggs_loc)
    assert azimuth.rad_val == pytest.approx(4.900004198967812, util.EPSILON)
    assert distance2.rad_val == pytest.approx(distance1.rad_val, util.EPSILON)

    temp_loc = gc.GreatCircle.dazgc(wh_loc, azimuth, distance2)
    assert temp_loc == skaggs_loc


def test_long0():
    """test great circle crossing longitude zero"""
    augsburg_lat = util.Latitude(48.45, False)
    augsburg_lng = util.Longitude(10.863611, False)
    augsburg_loc = util.Location(augsburg_lat, augsburg_lng)

    wh_lat = util.Latitude(44.401111, False)
    wh_lng = util.Longitude(-67.991111, False)
    wh_loc = util.Location(wh_lat, wh_lng)

    # winter harbor to augsburg
    (azimuth, distance1) = gc.GreatCircle.gcdaz(wh_loc, augsburg_loc)
    assert azimuth.rad_val == pytest.approx(0.9710389465471333, util.EPSILON)
    assert distance1.rad_val == pytest.approx(0.9081281026712691, util.EPSILON)

    temp_loc = gc.GreatCircle.dazgc(wh_loc, azimuth, distance1)
    assert temp_loc == augsburg_loc

    # augsburg to winter harbor
    (azimuth, distance2) = gc.GreatCircle.gcdaz(augsburg_loc, wh_loc)
    assert azimuth.rad_val == pytest.approx(5.187645334923327, util.EPSILON)
    assert distance2.rad_val == pytest.approx(distance1.rad_val, util.EPSILON)

    temp_loc = gc.GreatCircle.dazgc(augsburg_loc, azimuth, distance2)
    assert temp_loc == wh_loc


def test_long180():
    """test great circle crossing longitude 180"""
    wahiawa_lat = util.Latitude(21.522222, False)
    wahiawa_lng = util.Longitude(-158.011389, False)
    wahiawa_loc = util.Location(wahiawa_lat, wahiawa_lng)

    finegayan_lat = util.Latitude(13.593611, False)
    finegayan_lng = util.Longitude(144.8525, False)
    finegayan_loc = util.Location(finegayan_lat, finegayan_lng)

    # wahiawa to finegayan
    (azimuth, distance1) = gc.GreatCircle.gcdaz(wahiawa_loc, finegayan_loc)
    assert azimuth.rad_val == pytest.approx(4.74318012298315, util.EPSILON)
    assert distance1.rad_val == pytest.approx(0.9558762231057704, util.EPSILON)

    temp_loc = gc.GreatCircle.dazgc(wahiawa_loc, azimuth, distance1)
    assert temp_loc == finegayan_loc

    # finegayan to wahiawa
    (azimuth, distance2) = gc.GreatCircle.gcdaz(finegayan_loc, wahiawa_loc)
    assert azimuth.rad_val == pytest.approx(1.2752128093668078, util.EPSILON)
    assert distance2.rad_val == pytest.approx(distance1.rad_val, util.EPSILON)

    temp_loc = gc.GreatCircle.dazgc(finegayan_loc, azimuth, distance2)
    assert temp_loc == wahiawa_loc


def test_north_pole():
    """exercise great circle around north pole"""
    adak_lat = util.Latitude(51.9425, False)
    adak_lng = util.Longitude(-176.600556, False)
    adak_loc = util.Location(adak_lat, adak_lng)

    edzell_lat = util.Latitude(56.809167, False)
    edzell_lng = util.Longitude(-2.605556, False)
    edzell_loc = util.Location(edzell_lat, edzell_lng)

    # adak to edzell
    (azimuth, distance1) = gc.GreatCircle.gcdaz(adak_loc, edzell_loc)
    assert azimuth.rad_val == pytest.approx(0.06055698411302806, util.EPSILON)
    assert distance1.rad_val == pytest.approx(1.241561805890704, util.EPSILON)

    temp_loc = gc.GreatCircle.dazgc(adak_loc, azimuth, distance1)
    assert temp_loc == edzell_loc

    # edzell to adak
    (azimuth, distance2) = gc.GreatCircle.gcdaz(edzell_loc, adak_loc)
    assert azimuth.rad_val == pytest.approx(6.214981799746803, util.EPSILON)
    assert distance2.rad_val == pytest.approx(distance1.rad_val, util.EPSILON)

    temp_loc = gc.GreatCircle.dazgc(edzell_loc, azimuth, distance2)
    assert temp_loc == adak_loc

#
# Title: gcircle_test.py
# Description: test for GreatCircle
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import math
import pytest

import gcircle
import utility

def test_gcrab1():
    """source to dest is north"""
    source_lat = utility.DdAngle(0.0, False)
    source_lng = utility.DdAngle(0.0, False)
    source_loc = utility.Location(source_lat, source_lng)

    dest_lat = utility.DdAngle(2.0, False)
    dest_lng = utility.DdAngle(0.0, False)
    dest_loc = utility.Location(dest_lat, dest_lng)

    gc = gcircle.GreatCircle()
    (range, bearing) = gc.gcrab(source_loc, dest_loc)
    assert range.radian_value == 0.03490658503988567
    assert bearing.radian_value == 0.0

    converter = utility.Converter()
    print(f"gcrab1 {converter.arc2sm(range.radian_value)} {math.degrees(bearing.radian_value)}")
    #assert False

def test_gcrab2():
    """source to dest is north east"""
    source_lat = utility.DdAngle(0.0, False)
    source_lng = utility.DdAngle(0.0, False)
    source_loc = utility.Location(source_lat, source_lng)

    dest_lat = utility.DdAngle(2.0, False)
    dest_lng = utility.DdAngle(2.0, False)
    dest_loc = utility.Location(dest_lat, dest_lng)

    gc = gcircle.GreatCircle()
    (range, bearing) = gc.gcrab(source_loc, dest_loc)
    assert range.radian_value == 0.04936035239379336
    assert bearing.radian_value == 0.7850934841152278

    converter = utility.Converter()
    print(f"gcrab2 {converter.arc2sm(range.radian_value)} {math.degrees(bearing.radian_value)}")
    #assert False

def test_gcrab3():
    """source to dest is east"""
    source_lat = utility.DdAngle(0.0, False)
    source_lng = utility.DdAngle(0.0, False)
    source_loc = utility.Location(source_lat, source_lng)

    dest_lat = utility.DdAngle(0.0, False)
    dest_lng = utility.DdAngle(2.0, False)
    dest_loc = utility.Location(dest_lat, dest_lng)

    gc = gcircle.GreatCircle()
    (range, bearing) = gc.gcrab(source_loc, dest_loc)
    assert range.radian_value == 0.03490658503988567
    assert bearing.radian_value == 1.5707963267948966

    converter = utility.Converter()
    print(f"gcrab3 {converter.arc2sm(range.radian_value)} {math.degrees(bearing.radian_value)}")
    #assert False

def test_gcrab4():
    """source to dest is south east"""
    source_lat = utility.DdAngle(0.0, False)
    source_lng = utility.DdAngle(0.0, False)
    source_loc = utility.Location(source_lat, source_lng)

    dest_lat = utility.DdAngle(-2.0, False)
    dest_lng = utility.DdAngle(2.0, False)
    dest_loc = utility.Location(dest_lat, dest_lng)

    gc = gcircle.GreatCircle()
    (range, bearing) = gc.gcrab(source_loc, dest_loc)
    assert range.radian_value == 0.04936035239379336
    assert bearing.radian_value == 2.3564991694745654 

    converter = utility.Converter()
    print(f"gcrab4 {converter.arc2sm(range.radian_value)} {math.degrees(bearing.radian_value)}")
    #assert False

def test_gcrab5():
    """source to dest is south"""
    source_lat = utility.DdAngle(0.0, False)
    source_lng = utility.DdAngle(0.0, False)
    source_loc = utility.Location(source_lat, source_lng)

    dest_lat = utility.DdAngle(-2.0, False)
    dest_lng = utility.DdAngle(0.0, False)
    dest_loc = utility.Location(dest_lat, dest_lng)

    gc = gcircle.GreatCircle()
    (range, bearing) = gc.gcrab(source_loc, dest_loc)
    assert range.radian_value == 0.03490658503988567
    assert bearing.radian_value == 3.141592653589793 

    converter = utility.Converter()
    print(f"gcrab5 {converter.arc2sm(range.radian_value)} {math.degrees(bearing.radian_value)}")
    #assert False

def test_gcrab6():
    """source to dest is south west"""
    source_lat = utility.DdAngle(0.0, False)
    source_lng = utility.DdAngle(0.0, False)
    source_loc = utility.Location(source_lat, source_lng)

    dest_lat = utility.DdAngle(-2.0, False)
    dest_lng = utility.DdAngle(-2.0, False)
    dest_loc = utility.Location(dest_lat, dest_lng)

    gc = gcircle.GreatCircle()
    (range, bearing) = gc.gcrab(source_loc, dest_loc)
    assert range.radian_value == 0.04936035239379336
    assert bearing.radian_value == 3.926686137705021 

    converter = utility.Converter()
    print(f"gcrab6 {converter.arc2sm(range.radian_value)} {math.degrees(bearing.radian_value)}")
    #assert False

def test_gcrab7():
    """source to dest is west"""
    source_lat = utility.DdAngle(0.0, False)
    source_lng = utility.DdAngle(0.0, False)
    source_loc = utility.Location(source_lat, source_lng)

    dest_lat = utility.DdAngle(0.0, False)
    dest_lng = utility.DdAngle(-2.0, False)
    dest_loc = utility.Location(dest_lat, dest_lng)

    gc = gcircle.GreatCircle()
    (range, bearing) = gc.gcrab(source_loc, dest_loc)
    assert range.radian_value == 0.03490658503988567
    assert bearing.radian_value == 4.71238898038469 

    converter = utility.Converter()
    print(f"gcrab7 {converter.arc2sm(range.radian_value)} {math.degrees(bearing.radian_value)}")
    #assert False

def test_gcrab8():
    """source to dest is north west"""
    source_lat = utility.DdAngle(0.0, False)
    source_lng = utility.DdAngle(0.0, False)
    source_loc = utility.Location(source_lat, source_lng)

    dest_lat = utility.DdAngle(2.0, False)
    dest_lng = utility.DdAngle(-2.0, False)
    dest_loc = utility.Location(dest_lat, dest_lng)

    gc = gcircle.GreatCircle()
    (range, bearing) = gc.gcrab(source_loc, dest_loc)
    assert range.radian_value == 0.04936035239379336
    assert bearing.radian_value == 5.4980918230643585

    converter = utility.Converter()
    print(f"gcrab8 {converter.arc2sm(range.radian_value)} {math.degrees(bearing.radian_value)}")
    #assert False

def test_gcraz1():
    """source to dest is north"""
    source_lat = utility.DdAngle(0.0, False)
    source_lng = utility.DdAngle(0.0, False)
    source_loc = utility.Location(source_lat, source_lng)

    converter = utility.Converter()

    range = utility.DdAngle(converter.sm2arc(200.0), True)
    azimuth = utility.DdAngle(0.0, True)

    gc = gcircle.GreatCircle()
    dest_loc = gc.razgc(source_loc, range, azimuth)
    print(f"gcraz1 {dest_loc.lat.dd_value}:{dest_loc.lng.dd_value}")
#    assert False

def test_gcraz2():
    """source to dest is north east"""
    source_lat = utility.DdAngle(0.0, False)
    source_lng = utility.DdAngle(0.0, False)
    source_loc = utility.Location(source_lat, source_lng)

    converter = utility.Converter()

    range = utility.DdAngle(converter.sm2arc(200.0), True)
    azimuth = utility.DdAngle(math.pi/4, True)

    gc = gcircle.GreatCircle()
    dest_loc = gc.razgc(source_loc, range, azimuth)
    print(dest_loc)
    print(f"gcraz2 {dest_loc.lat.dd_value}:{dest_loc.lng.dd_value}")
#    assert False

def test_gcraz3():
    """source to dest is east"""
    source_lat = utility.DdAngle(0.0, False)
    source_lng = utility.DdAngle(0.0, False)
    source_loc = utility.Location(source_lat, source_lng)

    converter = utility.Converter()

    range = utility.DdAngle(converter.sm2arc(200.0), True)
    azimuth = utility.DdAngle(math.pi/2, True)

    gc = gcircle.GreatCircle()
    dest_loc = gc.razgc(source_loc, range, azimuth)
    print(dest_loc)
    print(f"gcraz3 {dest_loc.lat.dd_value}:{dest_loc.lng.dd_value}")
#    assert False

def test_gcraz4():
    """source to dest is south east"""
    source_lat = utility.DdAngle(0.0, False)
    source_lng = utility.DdAngle(0.0, False)
    source_loc = utility.Location(source_lat, source_lng)

    converter = utility.Converter()

    range = utility.DdAngle(converter.sm2arc(200.0), True)
    azimuth = utility.DdAngle(3*math.pi/4, True)

    gc = gcircle.GreatCircle()
    dest_loc = gc.razgc(source_loc, range, azimuth)
    print(dest_loc)
    print(f"gcraz4 {dest_loc.lat.dd_value}:{dest_loc.lng.dd_value}")
#    assert False

def test_gcraz5():
    """source to dest is south"""
    source_lat = utility.DdAngle(0.0, False)
    source_lng = utility.DdAngle(0.0, False)
    source_loc = utility.Location(source_lat, source_lng)

    converter = utility.Converter()

    range = utility.DdAngle(converter.sm2arc(200.0), True)
    azimuth = utility.DdAngle(math.pi, True)

    gc = gcircle.GreatCircle()
    dest_loc = gc.razgc(source_loc, range, azimuth)
    print(dest_loc)
    print(f"gcraz5 {dest_loc.lat.dd_value}:{dest_loc.lng.dd_value}")
#    assert False

def test_gcraz6():
    """source to dest is south west"""
    source_lat = utility.DdAngle(0.0, False)
    source_lng = utility.DdAngle(0.0, False)
    source_loc = utility.Location(source_lat, source_lng)

    converter = utility.Converter()

    range = utility.DdAngle(converter.sm2arc(200.0), True)
    azimuth = utility.DdAngle(5*math.pi/4, True)

    gc = gcircle.GreatCircle()
    dest_loc = gc.razgc(source_loc, range, azimuth)
    print(dest_loc)
    print(f"gcraz6 {dest_loc.lat.dd_value}:{dest_loc.lng.dd_value}")
#    assert False

def test_gcraz7():
    """source to dest is west"""
    source_lat = utility.DdAngle(0.0, False)
    source_lng = utility.DdAngle(0.0, False)
    source_loc = utility.Location(source_lat, source_lng)

    converter = utility.Converter()

    range = utility.DdAngle(converter.sm2arc(200.0), True)
    azimuth = utility.DdAngle(3*math.pi/2, True)

    gc = gcircle.GreatCircle()
    dest_loc = gc.razgc(source_loc, range, azimuth)
    print(dest_loc)
    print(f"gcraz7 {dest_loc.lat.dd_value}:{dest_loc.lng.dd_value}")
#    assert False

def test_gcraz8():
    """source to dest is north west"""
    source_lat = utility.DdAngle(0.0, False)
    source_lng = utility.DdAngle(0.0, False)
    source_loc = utility.Location(source_lat, source_lng)

    converter = utility.Converter()

    range = utility.DdAngle(converter.sm2arc(200.0), True)
    azimuth = utility.DdAngle(7*math.pi/4, True)

    gc = gcircle.GreatCircle()
    dest_loc = gc.razgc(source_loc, range, azimuth)
    print(dest_loc)
    print(f"gcraz8 {dest_loc.lat.dd_value}:{dest_loc.lng.dd_value}")
#    assert False
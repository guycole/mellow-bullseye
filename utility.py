#
# Title: utility.py
# Description: helper class and methods
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import math
import typing

EPSILON = 1e-6
PI_HALF = math.pi / 2.0


class DdAngle:
    """decimal degress container"""

    def __init__(self, value: float, radian_flag: bool):
        if radian_flag:
            self.dd_value = math.degrees(value)
            self.radian_value = value
        else:
            self.dd_value = value
            self.radian_value = math.radians(value)

    def __repr__(self):
        return str(self.dd_value)

    def __str__(self):
        return str(self.dd_value)

    def __hash__(self):
        return hash(self.radian_value)

    def __eq__(self, other):
        try:
            temp1 = abs(self.radian_value)
            temp2 = abs(other.radian_value)
            return abs(temp1-temp2) < EPSILON
        except AttributeError:
            return NotImplemented

class Latitude(DdAngle):
    """latitude in decimal degrees"""

    def __init__(self, value: float, rad_flag: bool):
        super().__init__(value, rad_flag)

        if abs(self.radian_value) > PI_HALF:
            raise ValueError("latitude exceeds 90 degrees")


class Longitude(DdAngle):
    """longitude in decimal degrees"""

    def __init__(self, value: float, rad_flag):
        super().__init__(value, rad_flag)

        if abs(self.radian_value) > math.pi:
            raise ValueError("longitude exceeds 180 degrees")


class Location:
    """coordinate as a latitude (+ north), longitude (+ east)"""

    def __init__(self, latitude: Latitude, longitude: Longitude):
        self.lat = latitude
        self.lng = longitude

    def __repr__(self):
        return f"{self.lat}:{self.lng}"

    def __str__(self):
        return f"{self.lat}:{self.lng}"

    def __hash__(self):
        return hash(f"{self.lat}:{self.lng}")

    def __eq__(self, other):
        try:
            return self.lat == other.lat and self.lng == other.lng
        except AttributeError:
            return NotImplemented

class Converter:
    """simple conversion routines"""

    def arc2sm(self, arg: float) -> float:
        """arc to statute miles"""
        return arg * 3958.8

    def sm2arc(self, arg: float) -> float:
        return arg / 3958.8

    def arc2klik(self, arg: float) -> float:
        """arc to kilometers"""
        return arg * 6378.1


if __name__ == "__main__":
    print("main")

    dd1 = DdAngle(12.3456, False)
    print(dd1)

    lat1 = Latitude(dd1.dd_value, False)
    print(lat1)

    lng1 = Longitude(dd1.dd_value, False)
    print(lng1)

#
# Title: utility.py
# Description: helper class and methods
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import math
import typing

EPSILON = 1e-6
FINAGLE = 1e6
PI_HALF = math.pi/2.0


class DmsAngle:
    """degrees, minutes, seconds container"""

    def __init__(self, degree: int, minute: int, second: float):
        self.dms_degree = degree
        self.dms_minute = minute
        self.dms_second = second

        decimal_degree = abs(degree)
        decimal_minute = minute / 60.0
        decimal_second = second / 3600.0

        # restrict the precision
        temp = round((decimal_minute + decimal_second) * FINAGLE)
        self.dms_converted = decimal_degree + temp / FINAGLE

        # self.dms_converted = decimal_degree + decimal_minute + decimal_second
        if degree < 0.0:
            self.dms_converted = self.dms_converted * -1.0

    def __repr__(self):
        return str(self.dms_converted)

    def __str__(self):
        return f"{self.dms_degree}-{self.dms_minute}-{self.dms_second}"

    def __hash__(self):
        return hash(self.dms_converted)

    def __eq__(self, other):
        try:
            flag1 = self.dms_converted < 0.0
            flag2 = other.dms_converted < 0.0

            if flag1 == flag2:
                delta = self.dms_converted - other.dms_converted
                return abs(delta) < EPSILON
            else:
                return False
        except AttributeError:
            return NotImplemented


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
            flag1 = self.radian_value < 0.0
            flag2 = other.radian_value < 0.0

            if flag1 == flag2:
                delta = self.radian_value - other.radian_value
                return abs(delta) < EPSILON
            else:
                return False
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
        return arg * 3963.3

    def sm2arc(self, arg: float) -> float:
        return arg/3963.3

    def arc2klik(self, arg: float) -> float:
        """arc to kilometers"""
        return arg * 6378.3

if __name__ == "__main__":
    print("main")

    dms1 = DmsAngle(11, 22, 33.44)
    print(dms1)

    dd1 = DdAngle(12.3456)
    print(dd1)

    lat1 = Latitude(dd1)
    print(lat1)

    lng1 = Longitude(dd1)
    print(lng1)

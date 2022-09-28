#
# Title: utility.py
# Description: helper class and methods
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import json
import math

EPSILON = 1e-6
PI_HALF = math.pi / 2.0


class DdAngle:
    """decimal degree container"""

    def __init__(self, value: float, rad_flag: bool):
        """construct a decimal degree container

        Args:
            value (float): angle value (radians or decimal degrees)
            radian_flag (bool): true, the value is radians else decimal degrees
        """

        if rad_flag:
            self.dd_val = math.degrees(value)
            self.rad_val = value
        else:
            self.dd_val = value
            self.rad_val = math.radians(value)

    def __repr__(self):
        return str(self.dd_val)

    def __str__(self):
        return str(self.dd_val)

    def __hash__(self):
        return hash(self.rad_val)

    def __eq__(self, other):
        return abs(self.rad_val - other.rad_val) < EPSILON

    def to_json(self):
        """convert the instance of this class to json"""
        return json.dumps(self, indent=4, default=lambda o: o.__dict__)


class Latitude(DdAngle):
    """latitude container"""

    def __init__(self, value: float, rad_flag: bool):
        """construct a latitude container

        Args:
            value (float): latitude (radians or decimal degrees) +North
            rad_flag (bool): true, the value is radians else decimal degrees

        Raises:
            ValueError: if value greater than 90 degrees
        """

        super().__init__(value, rad_flag)

        if abs(self.rad_val) > PI_HALF:
            raise ValueError("latitude exceeds 90 degrees")

    def to_json(self):
        """convert the instance of this class to json"""
        return json.dumps(self, indent=4, default=lambda o: o.__dict__)


class Longitude(DdAngle):
    """longitude container"""

    def __init__(self, value: float, rad_flag: bool):
        """construct a longitude container

        Args:
            value (float): longitude (radians or decimal degrees) +East
            rad_flag (bool): true, the valus is radians else decimal degrees

        Raises:
            ValueError: if value greater than 180 degrees
        """

        super().__init__(value, rad_flag)

        if abs(self.rad_val) > math.pi:
            raise ValueError("longitude exceeds 180 degrees")

    def to_json(self):
        """convert the instance of this class to json"""
        return json.dumps(self, indent=4, default=lambda o: o.__dict__)


class Location:
    """location container"""

    def __init__(self, latitude: Latitude, longitude: Longitude):
        """construct a location container

        Args:
            latitude (Latitude): latitude
            longitude (Longitude): longitude
        """

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

    def to_json(self):
        """convert the instance of this class to json"""
        return json.dumps(self, indent=4, default=lambda o: o.__dict__)


class Converter:
    """conversion support"""

    @staticmethod
    def arc2sm(arg: float) -> float:
        """arc radians to statute miles

        Args:
            arg (float): arc radians

        Returns:
            float: distance in statute miles
        """
        return arg * 3958.8

    @staticmethod
    def sm2arc(arg: float) -> float:
        """statute miles to arc radians

        Args:
            arg (float): distance in statute miles

        Returns:
            float: arc radians
        """
        return arg / 3958.8

    @staticmethod
    def arc2klik(arg: float) -> float:
        """arc radians to kilometers

        Args:
            arg (float): arc radians

        Returns:
            float: distance in kilometers
        """
        return arg * 6378.1


class FortranFunction:
    """replace missing FORTRAN functions"""

    @staticmethod
    def amin1(arg1, arg2):
        """return the minimum value

        Args:
            arg1 (_type_): argument
            arg2 (_type_): argument

        Returns:
            _type_: return the lowest value
        """
        if arg1 < arg2:
            return arg1

        return arg2

    @staticmethod
    def amax1(arg1, arg2):
        """return the maximum value

        Args:
            arg1 (_type_): argument
            arg2 (_type_): argument

        Returns:
            _type_: return the maximum value
        """
        if arg1 < arg2:
            return arg2

        return arg1

    @staticmethod
    def sign(arg1, arg2):
        """return the value of arg1 with the sign of arg2

        Args:
            arg1 (_type_): argument
            arg2 (_type_): argument

        Returns:
            _type_: return the value of arg1 with the sign of arg2
        """

        if arg2 < 0:
            if arg1 < 0:
                return arg1

            return -arg1

        if arg1 < 0:
            return -arg1

        return arg1


if __name__ == "__main__":
    print("main")

    dd1 = DdAngle(12.3456, False)
    print(dd1)

    lat1 = Latitude(dd1.dd_val, False)
    print(lat1)

    lng1 = Longitude(dd1.dd_val, False)
    print(lng1)

    loc1 = Location(lat1, lng1)
    print(loc1)

#
# Title: gcircle.py
# Description: great circle class and methods
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import math
import typing

import utility


class GreatCircle:
    def gcrab(self, source: utility.Location, destination: utility.Location) -> typing.Tuple[utility.DdAngle, utility.DdAngle]:
        """calculate great circle range and bearing between two points"""

        if abs(source.lat.radian_value - utility.PI_HALF) <= utility.EPSILON:
            # source is north pole
            range = utility.DdAngle(utility.PI_HALF - destination.lat.radian_value, True)
            azimuth = utility.DdAngle(math.pi, True)
            return (range, azimuth)

        if abs(source.lat.radian_value + utility.PI_HALF) <= utility.EPSILON:
            # source is south pole
            range = utility.DdAngle(utility.PI_HALF + destination.lat.radian_value, True)
            azimuth = utility.DdAngle(0.0, True)
            return (range, azimuth)

        lat_delta = abs(source.lat.radian_value - destination.lat.radian_value)
        lng_delta = abs(source.lng.radian_value - destination.lng.radian_value)
        if lat_delta < utility.EPSILON and lng_delta < utility.EPSILON:
            # coincident location
            range = utility.DdAngle(utility.EPSILON, True)
            azimuth = utility.DdAngle(0.0, True)
            return (range, azimuth)

        csn1 = math.cos(source.lng.radian_value)
        snn1 = math.sin(source.lng.radian_value)

        cst1 = math.cos(source.lat.radian_value)
        snt1 = math.sin(source.lat.radian_value)

        csn2 = math.cos(destination.lng.radian_value)
        snn2 = math.sin(destination.lng.radian_value)

        cst2 = math.cos(destination.lat.radian_value)
        snt2 = math.sin(destination.lat.radian_value)

        range = csn1 * cst1 * csn2 * cst2 + snn1 * cst1 * snn2 * cst2 + snt1 * snt2
        range = utility.DdAngle(math.acos(range), True)
        azimuth = utility.DdAngle(0.0, True)

        if range.radian_value > utility.EPSILON:
            xx = -csn1 * snt1 * csn2 * cst2 - snn1 * snt1 * snn2 * cst2 + cst1 * snt2
            yy = -snn1 * csn2 * cst2 + csn1 * snn2 * cst2
            azimuth = utility.DdAngle(math.atan2(yy, xx), True)
            if azimuth.radian_value < 0.0:
                # azimuth 0 is north, positive clockwise 
                azimuth = utility.DdAngle(azimuth.radian_value + math.pi * 2.0, True)

        return (range, azimuth)

    def razgc(
        self, source: utility.Location, range: utility.DdAngle, azimuth: utility.DdAngle
    ) -> utility.Location:
        """calculate great circle location given origin, range and distance"""

        csnf = math.cos(source.lng.radian_value)
        snnf = math.sin(source.lng.radian_value)

        cstf = math.cos(source.lat.radian_value)
        sntf = math.sin(source.lat.radian_value)

        csb = math.cos(azimuth.radian_value)
        snb = math.sin(azimuth.radian_value)

        csd = math.cos(range.radian_value)
        snd = math.sin(range.radian_value)

        rxf = csnf * cstf
        ryf = snnf * cstf
        rzf = sntf

        bxf = -snnf * snb - csnf * sntf * csb
        byf = csnf * snb - snnf * sntf * csb
        bzf = cstf * csb

        rxt = rxf * csd + bxf * snd
        ryt = ryf * csd + byf * snd
        rzt = rzf * csd + bzf * snd

        lat1 = math.atan2(rzt, math.sqrt(rxt * rxt + ryt * ryt))
        lng1 = math.atan2(ryt, rxt)

        lat = utility.Latitude(lat1, True)
        lng = utility.Longitude(lng1, True)
        return utility.Location(lat, lng)


if __name__ == "__main__":
    print("main")

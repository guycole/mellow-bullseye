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
    """
    great circle support
    """

    def gcdaz(
        self, source: utility.Location, destination: utility.Location
    ) -> typing.Tuple[utility.DdAngle, utility.DdAngle]:
        """
        Calculate great circle distance and azimuth between two points on earths surface.
        Originally written in FORTRAN by Jim Martin, 1985

        Args:
            source (utility.Location): source location
            destination (utility.Location): destination location

        Returns:
            typing.Tuple[utility.DdAngle, utility.DdAngle]: azimuth, distance
        """

        if source == destination:
            # coincident location
            azimuth = utility.DdAngle(0.0, True)
            distance = utility.DdAngle(0.0, True)
            return (azimuth, distance)

        if abs(source.lat.rad_val - utility.PI_HALF) < utility.EPSILON:
            # source is north pole
            azimuth = utility.DdAngle(math.pi, True)
            distance = utility.DdAngle(utiity.PI_HALF - destination.lat.rad_val, True)
            return (azimuth, distance)

        if abs(source.lat.rad_val + utility.PI_HALF) < utility.EPSILON:
            # source is south pole
            azimuth = utility.DdAngle(0.0, True)
            distance = utility.DdAngle(utiity.PI_HALF + destination.lat.rad_val, True)
            return (azimuth, distance)

        csn1 = math.cos(source.lng.rad_val)
        snn1 = math.sin(source.lng.rad_val)

        cst1 = math.cos(source.lat.rad_val)
        snt1 = math.sin(source.lat.rad_val)

        csn2 = math.cos(destination.lng.rad_val)
        snn2 = math.sin(destination.lng.rad_val)

        cst2 = math.cos(destination.lat.rad_val)
        snt2 = math.sin(destination.lat.rad_val)

        temp = csn1 * cst1 * csn2 * cst2 + snn1 * cst1 * snn2 * cst2 + snt1 * snt2
        distance = utility.DdAngle(math.acos(temp), True)
        azimuth = utility.DdAngle(0.0, True)

        if distance.rad_val > utility.EPSILON:
            xx = -csn1 * snt1 * csn2 * cst2 - snn1 * snt1 * snn2 * cst2 + cst1 * snt2
            yy = -snn1 * csn2 * cst2 + csn1 * snn2 * cst2
            azimuth = utility.DdAngle(math.atan2(yy, xx), True)
            if azimuth.rad_val < 0.0:
                # azimuth 0 is north, positive clockwise
                azimuth = utility.DdAngle(azimuth.rad_val + math.pi * 2.0, True)

        return (azimuth, distance)

    def dazgc(
        self,
        source: utility.Location,
        azimuth: utility.DdAngle,
        distance: utility.DdAngle,
    ) -> utility.Location:
        """
        Given an source, azimuth and distance return a location

        Args:
            source (utility.Location): source location
            azimuth (utility.DdAngle): bearing (radians) from North, clockwise
            distance (utility.DdAngle): distance (radians)

        Returns:
            utility.Location: destination
        """

        csnf = math.cos(source.lng.rad_val)
        snnf = math.sin(source.lng.rad_val)

        cstf = math.cos(source.lat.rad_val)
        sntf = math.sin(source.lat.rad_val)

        csb = math.cos(azimuth.rad_val)
        snb = math.sin(azimuth.rad_val)

        csd = math.cos(distance.rad_val)
        snd = math.sin(distance.rad_val)

        rxf = csnf * cstf
        ryf = snnf * cstf
        rzf = sntf

        bxf = -snnf * snb - csnf * sntf * csb
        byf = csnf * snb - snnf * sntf * csb
        bzf = cstf * csb

        rxt = rxf * csd + bxf * snd
        ryt = ryf * csd + byf * snd
        rzt = rzf * csd + bzf * snd

        temp_lat = math.atan2(rzt, math.sqrt(rxt * rxt + ryt * ryt))
        temp_lng = math.atan2(ryt, rxt)

        lat = utility.Latitude(temp_lat, True)
        lng = utility.Longitude(temp_lng, True)
        return utility.Location(lat, lng)


if __name__ == "__main__":
    print("main")

    skaggs_lat = utility.Latitude(38.1793681, False)
    skaggs_lng = utility.Longitude(-122.3731450, False)
    skaggs_loc = utility.Location(skaggs_lat, skaggs_lng)
    print(skaggs_loc)

    wh_lat = utility.Latitude(44.401111, False)
    wh_lng = utility.Longitude(-67.991111, False)
    wh_loc = utility.Location(wh_lat, wh_lng)
    print(wh_loc)

    converter = utility.Converter()

    gc = GreatCircle()
    (azimuth, distance) = gc.gcdaz(skaggs_loc, wh_loc)

    print(f"skaggs island to winter harbor bearing {azimuth.dd_val}")
    print(
        f"skaggs island to winter harbor distance {converter.arc2sm(distance.rad_val)} SM"
    )

    temp_loc = gc.dazgc(skaggs_loc, azimuth, distance)
    print(f"new location: {temp_loc}")

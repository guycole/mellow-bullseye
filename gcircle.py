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
    def gcrab(
        self, source: utility.Location, destination: utility.Location
    ) -> typing.Tuple[utility.DdAngle, utility.DdAngle]:
        """calculate great circle range and bearing between two points"""

        if source == destination:
            # coincident location
            range = utility.DdAngle(0.0, True)
            azimuth = utility.DdAngle(0.0, True)
            return (range, azimuth)

        csn1 = math.cos(source.lng.rad_val)
        snn1 = math.sin(source.lng.rad_val)

        cst1 = math.cos(source.lat.rad_val)
        snt1 = math.sin(source.lat.rad_val)

        csn2 = math.cos(destination.lng.rad_val)
        snn2 = math.sin(destination.lng.rad_val)

        cst2 = math.cos(destination.lat.rad_val)
        snt2 = math.sin(destination.lat.rad_val)

        range = csn1 * cst1 * csn2 * cst2 + snn1 * cst1 * snn2 * cst2 + snt1 * snt2
        range = utility.DdAngle(math.acos(range), True)
        azimuth = utility.DdAngle(0.0, True)

        if range.rad_val > utility.EPSILON:
            xx = -csn1 * snt1 * csn2 * cst2 - snn1 * snt1 * snn2 * cst2 + cst1 * snt2
            yy = -snn1 * csn2 * cst2 + csn1 * snn2 * cst2
            azimuth = utility.DdAngle(math.atan2(yy, xx), True)
            if azimuth.rad_val < 0.0:
                # azimuth 0 is north, positive clockwise
                azimuth = utility.DdAngle(azimuth.rad_val + math.pi * 2.0, True)

        return (range, azimuth)

    def razgc(
        self, source: utility.Location, range: utility.DdAngle, azimuth: utility.DdAngle
    ) -> utility.Location:
        """calculate great circle location given origin, range and bearing"""

        csnf = math.cos(source.lng.rad_val)
        snnf = math.sin(source.lng.rad_val)

        cstf = math.cos(source.lat.rad_val)
        sntf = math.sin(source.lat.rad_val)

        csb = math.cos(azimuth.rad_val)
        snb = math.sin(azimuth.rad_val)

        csd = math.cos(range.rad_val)
        snd = math.sin(range.rad_val)

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
    (range, azimuth) = gc.gcrab(skaggs_loc, wh_loc)

    print(f"skaggs island to winter harbor bearing {azimuth.dd_val}")
    print(
        f"skaggs island to winter harbor distance {converter.arc2sm(range.rad_val)} SM"
    )

    temp_loc = gc.razgc(skaggs_loc, range, azimuth)
    print(f"new location: {temp_loc}")

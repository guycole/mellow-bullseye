#
# Title: utility.py
# Description: helper class and methods
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import math
import os
import typing

import utility


class Station:
    """container for stations"""

    def __init__(self, key: str, location: utility.Location):
        self.key = key
        self.location = location

    def __repr__(self):
        return f"{self.key}:{self.location}"

    def __str__(self):
        return f"{self.key}:{self.location}"

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        try:
            return self.key == other.key
        except AttributeError:
            return NotImplemented


class StationReader:
    def parser(self, buffer: str) -> Station:
        """parse a station row"""

        candidate = buffer.lower().strip()
        if candidate.startswith("#") or len(candidate) < 2:
            # skip comment or empty row
            return None

        row_tokens = candidate.split(" ")
        if len(row_tokens) != 3:
            print("skipping bad line")
            return None

        # latitude in the form 13-29-02.2224n
        lat_tokens = row_tokens[1].split("-")
        if len(lat_tokens) != 3:
            print("skipping bad latitude")
            return None

        degree = int(lat_tokens[0])
        minute = int(lat_tokens[1])
        second = float(lat_tokens[2][: len(lat_tokens[2]) - 1])

        if lat_tokens[2].endswith("n"):
            pass
        elif lat_tokens[2].endswith("s"):
            degree = degree * -1.0
        else:
            print("skipping bad latitude")
            return None

        dms_lat = utility.DmsAngle(degree, minute, second)
        dd_lat = utility.DdAngle(dms_lat.dms_converted, False)

        # longitude in the form 149-59-53.2950w
        lng_tokens = row_tokens[2].split("-")
        if len(lng_tokens) != 3:
            print("skipping bad longitude")
            return None

        degree = int(lng_tokens[0])
        minute = int(lng_tokens[1])
        second = float(lng_tokens[2][: len(lng_tokens[2]) - 1])

        if lng_tokens[2].endswith("e"):
            pass
        elif lng_tokens[2].endswith("w"):
            degree = degree * -1.0
        else:
            print("skipping bad longitude")
            return None

        dms_lng = utility.DmsAngle(degree, minute, second)
        dd_lng = utility.DdAngle(dms_lng.dms_converted, False)
        location = utility.Location(dd_lat, dd_lng)

        station = Station(row_tokens[0], location)
        return station

    def reader(self, file_name: str) -> typing.List[Station]:
        """read a station file and return list of stations"""

        buffer = []
        results = []

        if not os.path.isfile(file_name):
            print(f"missing station file {file_name}")
            return results

        try:
            with open(file_name, "r") as station_file:
                buffer = station_file.readlines()
        except:
            print("file read error")

        for current in buffer:
            parsed = self.parser(current)
            if parsed != None:
                results.append(parsed)

        return results


if __name__ == "__main__":
    print("main")

    sr = StationReader()
    results = sr.reader("stations.dat")
    print(results)

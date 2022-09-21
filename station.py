#
# Title: station.py
# Description: helper class and methods for managing stations
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import math
import os
import typing

import utility


class Station:
    """container for stations"""

    def __init__(
        self, key: str, equipment: str, variance: int, location: utility.Location
    ):
        self.equipment = equipment
        self.key = key.strip()
        self.location = location
        self.variance = variance

        # station key always 3 characters
        if len(self.key) != 3:
            raise ValueError("bad station key")

        # test for legal equipment
        legal_equipment = ["grd6", "frd10", "flr9", "pusher", "outboard", "experiment"]
        if equipment not in legal_equipment:
            raise ValueError("bad equipment type")

    def __repr__(self):
        return f"{self.key}:{self.equipment}:{self.location}"

    def __str__(self):
        return f"{self.key}:{self.equipment}:{self.location}"

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
        if candidate.startswith("#") or len(candidate) < 3:
            # skip comment or empty row
            return None

        row_tokens = candidate.split(" ")
        if len(row_tokens) != 5:
            print("skipping bad line")
            return None

        # latitude in dd form
        dd_lat = utility.DdAngle(float(row_tokens[3]), False)

        # longitude in dd form
        dd_lng = utility.DdAngle(float(row_tokens[4]), False)

        # location
        location = utility.Location(dd_lat, dd_lng)

        station = Station(row_tokens[0], row_tokens[1], row_tokens[2], location)
        return station

    def reader(self, file_name: str) -> typing.Dict[str, Station]:
        """read a station file and return dictionary of stations"""

        buffer = []
        results = {}

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
                results[parsed.key] = parsed

        return results


class StationManager:
    def __init__(self):
        self.stations = {}

    def read_stations(self, file_name: str) -> None:
        sr = StationReader()
        self.stations = sr.reader(file_name)

    def get_station(self, key: str) -> Station:
        return self.stations[key]


if __name__ == "__main__":
    print("main")

    sm = StationManager()
    sm.read_stations("stations.dat")
    print(sm.get_station("sea"))

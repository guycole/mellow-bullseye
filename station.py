#
# Title: station.py
# Description: helper class and methods for managing stations
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import os
import typing

import utility as util


class Station:
    """container for station domain object"""

    def __init__(
        self, key: str, equipment: str, variance: int, location: util.Location
    ):
        """construct a station container

        Args:
            key (str): three character identifier
            equipment (str): enumerated equipment type (i.e. frd10)
            variance (int): magnetic variance
            location (utility.Location): location

        Raises:
            ValueError: bad station key or equipment
        """

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
    """read and parse station file"""

    def parser(self, buffer: str) -> Station:
        """parse a station row

        Args:
            buffer (str): raw station

        Returns:
            Station: populated Station object
        """

        candidate = buffer.lower().strip()
        if candidate.startswith("#") or len(candidate) < 3:
            # skip comment or empty row
            return None

        row_tokens = candidate.split(" ")
        if len(row_tokens) != 5:
            print("skipping bad line")
            return None

        # latitude in dd form
        dd_lat = util.DdAngle(float(row_tokens[3]), False)

        # longitude in dd form
        dd_lng = util.DdAngle(float(row_tokens[4]), False)

        # location
        location = util.Location(dd_lat, dd_lng)

        station = Station(row_tokens[0], row_tokens[1], row_tokens[2], location)
        return station

    def reader(self, file_name: str) -> typing.Dict[str, Station]:
        """read a station file and return a dictionary of stations

        Args:
            file_name (str): file file name

        Returns:
            typing.Dict[str, Station]: dictionary of stations
        """

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
            if parsed is not None:
                results[parsed.key] = parsed

        return results


class StationManager:
    """station management API"""

    def __init__(self):
        self.stations = {}

    def read_stations(self, file_name: str) -> None:
        """read station file and cache contents"""
        sr = StationReader()
        self.stations = sr.reader(file_name)

    def get_station(self, key: str) -> Station:
        """return station associated with key"""
        return self.stations[key]


if __name__ == "__main__":
    print("main")

    sm = StationManager()
    sm.read_stations("stations.dat")
    print(sm.get_station("sea"))

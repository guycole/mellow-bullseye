#
# Title: case.py
# Description: helper class and methods
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import math
import os
import typing

import utility


class Observation:
    """container for observations"""

    def __init__(self, station: str, quality: str, bearing: float):
        self.station = station
        self.quality = quality
        self.bearing = bearing

    def __repr__(self):
        return f"{self.station}:{self.quality}:{self.bearing}"

    def __str__(self):
        return f"{self.station}:{self.quality}:{self.bearing}"

    def __hash__(self):
        return hash(self.station)

    def __eq__(self, other):
        try:
            return self.station == other.station
        except AttributeError:
            return NotImplemented


class Case:
    """container for case, id is the same as filename"""

    def __init__(self, id: str):
        self.id = id
        self.observations = []

    def __repr__(self):
        return f"{self.id}"

    def __str__(self):
        return f"{self.id}"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        try:
            return self.id == other.id
        except AttributeError:
            return NotImplemented


class CaseReader:
    def parser(self, case_id: str, buffer: typing.List[str]) -> Case:
        """parse a observation row"""
        case = Case(case_id)

        for current in buffer:
            candidate = current.lower().strip()
            if candidate.startswith("#") or len(candidate) < 2:
                # skip comment or empty row
                continue

            row_tokens = candidate.split(" ")
            if len(row_tokens) != 3:
                print("skipping bad line")
                continue

            obs = Observation(row_tokens[0], row_tokens[1], row_tokens[2])
            case.observations.append(obs)

        return case

    def reader(self, file_name: str) -> Case:
        """read and parse case file"""

        if not os.path.isfile(file_name):
            print(f"missing case file {file_name}")
            return None

        try:
            with open(file_name, "r") as case_file:
                buffer = case_file.readlines()
        except:
            print("file read error")
            return None

        tokens = file_name.split("/")
        case_id = tokens[len(tokens) - 1]

        return self.parser(case_id, buffer)


if __name__ == "__main__":
    print("main")

    case = CaseReader()
    result = case.reader("case/p00001")
    print(result)
    print(result.observations)

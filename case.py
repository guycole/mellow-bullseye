#
# Title: case.py
# Description: helper class and methods
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import json
import math
import os
import time
import typing

import utility


class Observation:
    """container for observations"""

    def __init__(self, station: str, quality: str, bearing: utility.DdAngle):
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
        self.actual_location = None
        self.estimated_location = None
        self.time_stamp = int(time.time())

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
    def parser(self, buffer: dict) -> Case:
        """parse a case file"""

        case_id = buffer["case_id"]
        case = Case(case_id)

        print(buffer)

        if 'actual_location' in buffer:
            temp = buffer['actual_location']
            temp_lat = utility.DdAngle(temp[0], False)
            temp_lng = utility.DdAngle(temp[1], False)
            temp_loc = utility.Location(temp_lat, temp_lng)
            case.actual_location = temp_loc

        if 'estimated_location' in buffer:
            temp = buffer['estimated_location']
            temp_lat = utility.DdAngle(temp[0], False)
            temp_lng = utility.DdAngle(temp[1], False)
            temp_loc = utility.Location(temp_lat, temp_lng)
            case.estimated_location = temp_loc

        case.time_stamp = buffer['time_stamp']

        for ndx in buffer['observations']:
            obs = Observation(ndx[0], ndx[1], utility.DdAngle(ndx[2], False))
            case.observations.append(obs)

        return case

    def reader(self, file_name: str) -> Case:
        """read and parse case file"""

        if not os.path.isfile(file_name):
            print(f"missing case file {file_name}")
            return None

        try:
            with open(file_name, "r") as case_file:
                buffer = json.load(case_file)
        except:
            print("file read error")
            return None

        return self.parser(buffer)

class CaseWriter:
    def writer(self, file_name:str, case:Case) -> None:
        observations = []
        for current in case.observations:
            temp = [current.station, current.quality, current.bearing.dd_value]
            observations.append(temp)

        buffer = {}
        buffer['case_id'] = case.id
        buffer['time_stamp'] = case.time_stamp

        if case.actual_location is not None:
            buffer['actual_location'] = [case.actual_location.lat.dd_value, case.actual_location.lng.dd_value]

        if case.estimated_location is not None:
            buffer['estimated_location'] = [case.estimated_location.lat.dd_value, case.estimated_location.lng.dd_value]

        buffer['observations'] = observations
      
        try:
            with open(file_name, "w") as case_file:
                json.dump(buffer, case_file)
        except:
            print("file write error")
            return None

if __name__ == "__main__":
    print("main")

    cr = CaseReader()
    result = cr.reader("case/p00101")
    print(result)
    print(result.observations)

    cw = CaseWriter()
    cw.writer("case/ptest", result)
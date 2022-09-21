#
# Title: artifact.py
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
    """container for observations, nil heard/no bearing results are not retained"""

    def __init__(self, station: str, quality: str, id_certain: bool, bearing: utility.DdAngle):
        self.bearing = bearing
        self.bearing_used = False
        self.id_certain = id_certain
        self.quality = quality
        self.station = station
        self.weight = 0

        # todo test for legal bearing quality

    def __repr__(self):
        return f"{self.station}:{self.quality}:{self.id_certain}:{self.bearing}:{self.bearing_used}"

    def __str__(self):
        return f"{self.station}:{self.quality}:{self.id_certain}:{self.bearing}:{self.bearing_used}"

    def __hash__(self):
        return hash(self.station)

    def __eq__(self, other):
        try:
            return self.station == other.station
        except AttributeError:
            return NotImplemented


class Artifact:
    """artifact contains observations and fix results"""

    def __init__(self, id: str):
        self.actual_location = None 
        self.callsign = None
        self.ellipse_area = 0
        self.ellipse_location = None
        self.ellipse_major = 0
        self.ellipse_minor = 0
        self.ellipse_orientation = None
        self.fix_algorithm = None
        self.id = id
        self.observations = []
        self.radio_frequency = 0
        self.time_stamp = int(time.time()) # UTC epoch time
        self.version = 1

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


class ArtifactReadWrite:
    def parser(self, buffer: dict) -> Artifact:
        """parse a artifact file"""

        artifact = Artifact(buffer["id"])
        artifact.version = buffer["version"]

        # todo test for json schema version

        artifact.radio_frequency = buffer["radio_frequency"]
        artifact.time_stamp = buffer["time_stamp"]

        if "callsign" in buffer:
            artifact.callsign = buffer["callsign"]

        if "fix_algorithm" in buffer:
            artifact.fix_algorithm = buffer["fix_algorithm"]

        if "actual_location" in buffer:
            temp = buffer["actual_location"]
            temp_lat = utility.DdAngle(temp[0], False)
            temp_lng = utility.DdAngle(temp[1], False)
            temp_loc = utility.Location(temp_lat, temp_lng)
            artifact.actual_location = temp_loc

        if "ellipse_location" in buffer:
            temp = buffer["ellipse_location"]
            temp_lat = utility.DdAngle(temp[0], False)
            temp_lng = utility.DdAngle(temp[1], False)
            temp_loc = utility.Location(temp_lat, temp_lng)
            artifact.ellipse_location = temp_loc

            temp = buffer["ellipse_orientation"]
            artifact.ellipse_orientation = utility.DdAngle(temp, False)

            artifact.ellipse_area = buffer["ellipse_area"]
            artifact.ellipse_major = buffer["ellipse_major"]
            artifact.ellipse_minor = buffer["ellipse_minor"]

        for ndx in buffer["observations"]:
            obs = Observation(ndx[0], ndx[1], ndx[2], utility.DdAngle(ndx[3], False))
            obs.bearing_used = ndx[4]
            artifact.observations.append(obs)

        return artifact

    def reader(self, file_name: str) -> Artifact:
        """read and parse artifact file"""

        if not os.path.isfile(file_name):
            print(f"missing artifact file {file_name}")
            return None

        try:
            with open(file_name, "r") as artifact_file:
                buffer = json.load(artifact_file)
        except:
            print("file read error")
            return None

        return self.parser(buffer)

    def writer(self, file_name: str, artifact: Artifact) -> None:
        buffer = {}
        buffer["id"] = artifact.id
        buffer["radio_frequency"] = artifact.radio_frequency
        buffer["time_stamp"] = artifact.time_stamp
        buffer["version"] = 1

        if artifact.callsign is not None:
            buffer["callsign"] = artifact.callsign

        if artifact.fix_algorithm is not None:
            buffer["fix_algorithm"] = artifact.fix_algorithm

        if artifact.actual_location is not None:
            buffer["actual_location"] = [
                artifact.actual_location.lat.dd_val,
                artifact.actual_location.lng.dd_val,
            ]

        if artifact.ellipse_location is not None:
            buffer["ellipse_location"] = [
                artifact.ellipse_location.lat.dd_val,
                artifact.ellipse_location.lng.dd_val,
            ]

            buffer["ellipse_area"] = artifact.ellipse_area
            buffer["ellipse_major"] = artifact.ellipse_major
            buffer["ellipse_minor"] = artifact.ellipse_minor
            buffer["ellipse_orientation"] = artifact.ellipse_orientation.dd_val

        observations = []
        for current in artifact.observations:
            temp = [current.station, current.quality, current.id_certain, current.bearing.dd_val, current.bearing_used]
            observations.append(temp)

        buffer["observations"] = observations

        try:
            with open(file_name, "w") as artifact_file:
                json.dump(buffer, artifact_file)
        except:
            print("file write error")
            return None


if __name__ == "__main__":
    print("main")

    arw = ArtifactReadWrite()
    result = arw.reader("artifact_in/p00114")
    print(result)
    print(result.observations)

    arw.writer("artifact_out/ptest", result)

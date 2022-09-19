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


class Artifact:
    """container for artifact, id is the same as filename"""

    def __init__(self, id: str):
        self.id = id
        self.observations = []
        self.actual_location = None
        self.estimated_location = None
        self.time_stamp = int(time.time())
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

        # todo test for json schema version

        if "actual_location" in buffer:
            temp = buffer["actual_location"]
            temp_lat = utility.DdAngle(temp[0], False)
            temp_lng = utility.DdAngle(temp[1], False)
            temp_loc = utility.Location(temp_lat, temp_lng)
            artifact.actual_location = temp_loc

        if "estimated_location" in buffer:
            temp = buffer["estimated_location"]
            temp_lat = utility.DdAngle(temp[0], False)
            temp_lng = utility.DdAngle(temp[1], False)
            temp_loc = utility.Location(temp_lat, temp_lng)
            artifact.estimated_location = temp_loc

        artifact.time_stamp = buffer["time_stamp"]

        for ndx in buffer["observations"]:
            obs = Observation(ndx[0], ndx[1], utility.DdAngle(ndx[2], False))
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
        observations = []
        for current in artifact.observations:
            temp = [current.station, current.quality, current.bearing.dd_value]
            observations.append(temp)

        buffer = {}
        buffer["id"] = artifact.id
        buffer["time_stamp"] = artifact.time_stamp
        buffer["version"] = 1

        if artifact.actual_location is not None:
            buffer["actual_location"] = [
                artifact.actual_location.lat.dd_value,
                artifact.actual_location.lng.dd_value,
            ]

        if artifact.estimated_location is not None:
            buffer["estimated_location"] = [
                artifact.estimated_location.lat.dd_value,
                artifact.estimated_location.lng.dd_value,
            ]

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

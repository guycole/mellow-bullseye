#
# Title: artifact.py
# Description: helper class and methods
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import json
import os
import time

import utility as util


class Observation:
    """container for station observations"""

    def __init__(
        self,
        station: str,
        quality: str,
        id_certain: bool,
        bearing: util.DdAngle,
        equipment: str,
        location: util.Location,
    ):
        """construct a station observation

        Args:
            station (str): station identifier
            quality (str): bearing quality
            id_certain (bool): true, target identity confirmed
            bearing (utility.DdAngle): observed bearing to target
            equipment (str): enumerated equipment type
            location (utility.Location): station location
        """

        self.bearing = bearing
        self.bearing_used = True
        self.equipment = equipment
        self.error = 0
        self.id_certain = id_certain
        self.location = location
        self.quality = quality
        self.station = station
        self.weight = 1

        # todo test for legal bearing quality

    def __repr__(self):
        return f"{self.station}:{self.quality}:{self.id_certain}:{self.bearing}:{self.bearing_used}:{self.weight}"

    def __str__(self):
        return f"{self.station}:{self.quality}:{self.id_certain}:{self.bearing}:{self.bearing_used}:{self.weight}"

    def __hash__(self):
        return hash(self.station)

    def __eq__(self, other):
        try:
            return self.station == other.station
        except AttributeError:
            return NotImplemented

    def to_json(self):
        """convert the instance of this class to json"""
        return json.dumps(self, indent=4, default=lambda o: o.__dict__)


class Artifact:
    """container for all the task things"""

    def __init__(self, key: str):
        self.actual_location = None
        self.callsign = None
        self.ellipse_area = 0
        self.ellipse_location = None
        self.ellipse_major = 0
        self.ellipse_minor = 0
        self.ellipse_orientation = None
        self.fix_algorithm = None
        self.key = key
        self.observations = []
        self.radio_frequency = 0
        self.time_stamp = int(time.time())  # UTC epoch time
        self.version = 1

    def __repr__(self):
        return f"{self.key}"

    def __str__(self):
        return f"{self.key}"

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        try:
            return self.key == other.key
        except AttributeError:
            return NotImplemented

    def bearing_population(self):
        """return quantity of employed bearings"""
        population = 0
        for obs in self.observations:
            if obs.bearing_used:
                population += 1

        return population

    def to_json(self):
        """convert the instance of this class to json"""
        return json.dumps(self, indent=4, default=lambda o: o.__dict__)


class ArtifactReadWrite:
    """support for reading and writing artifacts"""

    def parser_v1(self, buffer: dict) -> Artifact:
        """parse a version 1 artifact file

        Args:
            buffer (dict): json dictionary

        Returns:
            Artifact: populated artifact object
        """
        artifact = Artifact(buffer["key"])

        artifact.callsign = buffer["callsign"]
        artifact.fix_algorithm = buffer["fix_algorithm"]
        artifact.radio_frequency = buffer["radio_frequency"]
        artifact.time_stamp = buffer["time_stamp"]
        artifact.version = buffer["version"]

        temp = buffer["actual_location"]
        if temp is not None:
            temp_lat = util.Latitude(temp["lat"]["dd_val"], False)
            temp_lng = util.Longitude(temp["lng"]["dd_val"], False)
            temp_loc = util.Location(temp_lat, temp_lng)
            artifact.actual_location = temp_loc

        temp = buffer["ellipse_location"]
        if temp is not None:
            temp_lat = util.Latitude(temp["lat"]["dd_val"], False)
            temp_lng = util.Longitude(temp["lng"]["dd_val"], False)
            temp_loc = util.Location(temp_lat, temp_lng)
            artifact.ellipse_location = temp_loc

        temp = buffer["ellipse_orientation"]
        if temp is not None:
            artifact.ellipse_orientation = util.DdAngle(temp, False)

        artifact.ellipse_area = buffer["ellipse_area"]
        artifact.ellipse_major = buffer["ellipse_major"]
        artifact.ellipse_minor = buffer["ellipse_minor"]

        for ndx in buffer["observations"]:
            bearing = util.DdAngle(ndx["bearing"]["dd_val"], False)
            bearing_used = ndx["bearing_used"]
            equipment = ndx["equipment"]
            id_certain = ndx["id_certain"]
            quality = ndx["quality"]
            station = ndx["station"]
            weight = ndx["weight"]

            temp = ndx["location"]
            temp_lat = util.Latitude(temp["lat"]["dd_val"], False)
            temp_lng = util.Longitude(temp["lng"]["dd_val"], False)
            temp_loc = util.Location(temp_lat, temp_lng)
            location = temp_loc

            obs = Observation(
                station, quality, id_certain, bearing, equipment, location
            )
            artifact.observations.append(obs)

        return artifact

    def reader(self, file_name: str) -> Artifact:
        """read artifact file and cause it to be parsed

        Args:
            file_name (str): full file name to artficat file

        Returns:
            Artifact: populated artifact file
        """

        if not os.path.isfile(file_name):
            print(f"missing artifact file {file_name}")
            return None

        try:
            with open(file_name, "r") as artifact_file:
                buffer = json.load(artifact_file)
                artifact_dict = json.loads(buffer)
        except:
            print("file read error")
            return None

        if artifact_dict["version"] == 1:
            return self.parser_v1(artifact_dict)

        print("unsupported artifact version")

        return None

    def writer(self, file_name: str, artifact: Artifact) -> None:
        """write artifact file

        Args:
            file_name (str): file to create or overwrite
            artifact (Artifact): artifact to persist
        """

        try:
            with open(file_name, "w") as artifact_file:
                json.dump(artifact.to_json(), artifact_file)
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

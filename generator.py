#
# Title: generator.py
# Description: simulate track history
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import math
import artifact
import gcircle
import station
import utility


class ArtifactGenerator:
    """create a well populated artifact"""

    def __init__(self, file_name):
        self.sm = station.StationManager()
        self.sm.read_stations(file_name)

    def generate_artifact(self, key: str, target_loc: utility.Location) -> artifact.Artifact:
        """create a well populated artifact"""
        results = artifact.Artifact(key)
        results.radio_frequency = 12345678 #12 MHz
        results.actual_location = target_loc

        gc = gcircle.GreatCircle()
        for ndx in self.sm.stations:
            station2 = self.sm.get_station(ndx)
            (azimuth, distance) = gc.gcdaz(station2.location, target_loc)
            obs = artifact.Observation(
                key, "A", True, azimuth, station2.equipment, station2.location
            )
            results.observations.append(obs)

        return results

    def write_artifact(self, candidate: artifact.Artifact) -> None:
        arw = artifact.ArtifactReadWrite()
        arw.writer(f"artifact_in/{candidate.key}", candidate)


class PacificTrack:
    """create a simulated pacific target track"""

    def track1(self):
        """generate pacific track 1"""
        converter = utility.Converter()
        rangex = utility.DdAngle(converter.sm2arc(500), True)
        bearing = utility.DdAngle(135.0, False)

        locations = []

        origin_lat = utility.Latitude(32.0, False)
        origin_lng = utility.Longitude(128.0, False)
        origin_loc = utility.Location(origin_lat, origin_lng)
        locations.append(origin_loc)

        gc = gcircle.GreatCircle()

        loc1 = origin_loc
        for ndx in range(4):
            loc2 = gc.dazgc(loc1, bearing, rangex)
            locations.append(loc2)
            loc1 = loc2

        bearing = utility.DdAngle(75.0, False)

        for ndx in range(4):
            loc2 = gc.dazgc(loc1, bearing, rangex)
            locations.append(loc2)
            loc1 = loc2

        bearing = utility.DdAngle(50.0, False)

        for ndx in range(6):
            loc2 = gc.dazgc(loc1, bearing, rangex)
            locations.append(loc2)
            loc1 = loc2

        ag = ArtifactGenerator("stations.dat")
        for ndx, _ in enumerate(locations):
            temp = f"{ndx:02}"
            key = "p001" + temp
            candidate = ag.generate_artifact(key, locations[ndx])
            ag.write_artifact(candidate)


if __name__ == "__main__":
    print("main")

    pt = PacificTrack()
    pt.track1()

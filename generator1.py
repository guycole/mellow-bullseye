#
# Title: generator1.py
# Description: simulate track history
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import math
import case
import gcircle
import station
import utility

class CaseGenerator:

    def __init__(self, file_name):
        self.sm = station.StationManager()
        self.sm.read_stations("stations.dat")

    def generate_case(self, case_id:str, target_loc:utility.Location) -> case.Case:
        results = case.Case(case_id)

        gc = gcircle.GreatCircle()
        for key in self.sm.stations:
            station = self.sm.get_station(key)
            (range, bearing) = gc.gcrab(station.location, target_loc)
            results.observations.append(case.Observation(key, "A", bearing))

        return results

    def write_case(self, candidate:case.Case) -> None:
        cw = case.CaseWriter()
        cw.writer(f"case/{candidate.id}", candidate)

if __name__ == "__main__":
    print("main")

    cg = CaseGenerator("stations.dat")

    lat1 = utility.Latitude(32.0, False)
    lng1 = utility.Longitude(128.0, False)
    loc1 = utility.Location(lat1, lng1)

    candidate = cg.generate_case("p00101", loc1)
    cg.write_case(candidate)

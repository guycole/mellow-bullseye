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
        results.actual_location = target_loc

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

    locations = []

    lat1 = utility.Latitude(32.0, False)
    lng1 = utility.Longitude(128.0, False)
    loc1 = utility.Location(lat1, lng1)
    locations.append(loc1)

    converter = utility.Converter()
    rangex = utility.DdAngle(converter.sm2arc(500), True)
    bearing = utility.DdAngle(135.0, False)

    gc = gcircle.GreatCircle()
    loc2 = gc.razgc(loc1, rangex, bearing)
    locations.append(loc2)
   
    loc3 = gc.razgc(loc2, rangex, bearing)
    locations.append(loc3)
   
    loc4 = gc.razgc(loc3, rangex, bearing)
    locations.append(loc4)

    loc5 = gc.razgc(loc4, rangex, bearing)
    locations.append(loc5)

    bearing = utility.DdAngle(75.0, False)

    loc6 = gc.razgc(loc5, rangex, bearing)
    locations.append(loc6)

    loc7 = gc.razgc(loc6, rangex, bearing)
    locations.append(loc7)

    loc8 = gc.razgc(loc7, rangex, bearing)
    locations.append(loc8)
   
    loc9 = gc.razgc(loc8, rangex, bearing)
    locations.append(loc9)

    bearing = utility.DdAngle(50.0, False)

    loc10 = gc.razgc(loc9, rangex, bearing)
    locations.append(loc10)

    loc11 = gc.razgc(loc10, rangex, bearing)
    locations.append(loc11)

    loc12 = gc.razgc(loc11, rangex, bearing)
    locations.append(loc12)

    loc13 = gc.razgc(loc12, rangex, bearing)
    locations.append(loc13)

    loc14 = gc.razgc(loc13, rangex, bearing)
    locations.append(loc14)

    loc15 = gc.razgc(loc14, rangex, bearing)
    locations.append(loc15)

    for ndx in range(len(locations)):
        temp = f"{ndx:02}"
        case_id = "p001" + temp
        candidate = cg.generate_case(case_id, locations[ndx])
        cg.write_case(candidate)

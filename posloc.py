#
# Title: posloc.py
# Description: posloc fix
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#

#
# From the original FORTRAN
#C               POSLOC IS A HFDF POSITION LOCATION ALGORITHM DESIGNED
#C               TO PROVIDE AN ESTIMATE OF THE LOCATION OF AN ACTIVE
#C               HF SIGNAL EMITTER USING AZIMUTHAL MEASUREMENTS OF THE
#C               DIRECTION OF ARRIVAL OF SIGNAL ENERGY BY TWO OR MORE DF
#C               SITES AT LOCATIONS EXPRESSED IN ABSOLUTE WGS COORDINATES.
#C               POSLOC PROVIDES THE ESTIMATE OF EMITTER LOCATION IN WGS
#C               COORDINATES: ELLIPTICAL & CIRCULAR AREAS OF UNCERTAINTY 
#C               ARE PROVIDED.
#

import artifact
import station

class PosLoc:
    """POSLOC fix algorithm"""

    def __init__(self, file_name):
        self.sm = station.StationManager()
        self.sm.read_stations(file_name)

    def pos_initial(self):
        pass

    def pddg(self, artifact: artifact.Artifact):
        for ndx in artifact.observations:
            station = self.sm.get_station(ndx.station)
            if station.equipment == 'grd6':
                ndx.weight = 0.1 # does original really discard grd6 bearings?
            else:
                ndx.weight = 1.0

    def convert(self):
        pass

    def xform(self):
        pass

    def xprodbpe(self, artifact:artifact.Artifact):
        obz = artifact.observations

        for ndx1, obs in enumerate(artifact.observations):
            print(ndx1)
            print(obs)
          

    def fix(self, artifact: artifact.Artifact):
        print("PosLoc")
    
        # id = station name
        # s1 = station lat rads
        # stalat = station lat degs
        # stalon = station lon degs
        # s2 = staion long rads
        # s3 = station sin lat
        # s4 = 0.03 (??)
        # c2 = station cos lat
        # n2 = type equipment?
        # b1 = bearing rads
        # b2 = bearing error
        # p2 = algo pass counter
        # n1 = flag
        # o1 = flag
        # w = bearing weight
        # c3 = mystery 18 element array 


        self.pos_initial()
        self.pddg(artifact)
        self.convert()
        self.xform()
        self.xprodbpe(artifact)

        print(artifact.observations)

#        artifact.estimated_location = fix_loc

if __name__ == "__main__":
    print("main")

    ar = artifact.ArtifactReadWrite()
    artifact = ar.reader("artifact_in/p00114")

    posloc = PosLoc("stations.dat")
    posloc.fix(artifact)
    print(artifact)

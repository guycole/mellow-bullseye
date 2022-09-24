#
# Title: posloc.py
# Description: posloc fix
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import artifact
import station

class PosLoc:
    """
    from the original FORTRAN
C               POSLOC IS A HFDF POSITION LOCATION ALGORITHM DESIGNED
C               TO PROVIDE AN ESTIMATE OF THE LOCATION OF AN ACTIVE
C               HF SIGNAL EMITTER USING AZIMUTHAL MEASUREMENTS OF THE
C               DIRECTION OF ARRIVAL OF SIGNAL ENERGY BY TWO OR MORE DF
C               SITES AT LOCATIONS EXPRESSED IN ABSOLUTE WGS COORDINATES.
C               POSLOC PROVIDES THE ESTIMATE OF EMITTER LOCATION IN WGS
C               COORDINATES: ELLIPTICAL & CIRCULAR AREAS OF UNCERTAINTY 
C               ARE PROVIDED.
    """

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
    # iterate through stations
    # t1 = b1(i) // LOB
    # b3 = cos(t1)
    # b4 = -sin(t1)
    # x8 = pi/2 - s1(i) // halfpi - station lat
    # c4 = -cos(x8)
    
            T1 = B1(I)
        B3 = COS(T1)
        B4 = -SIN(T1)
        X8 = PI/2 - S1(I)
        C4 = -COS(X8)

    # 

    def xprodbpe(self, artifact:artifact.Artifact):
        obz = artifact.observations

        for ndx1, obs1 in enumerate(artifact.observations):
            station1 = self.sm.get_station(obs1.station)

            if obs1.weight != 0:
                for ndx2, obs2 in enumerate(artifact.observations, ndx1+1):
                    print(f"{ndx1} {ndx2}")

                    w1 = obs1.weight * obs2.weight
                    if w1 != 0:           
                        station2 = self.sm.get_station(obs2.station)
                        if station1.location.lat == station2.location.lat:
                            print("lat match")
                        else:
                           print("lat not match")
     


                        print("not zero")
                    else:
                        print("zero")
        
# do 50 i = 1, L (all obs)
# if weight
# do 40 j = i+1, i1 (next obs)  
#

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

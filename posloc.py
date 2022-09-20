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

    def fix(self, artifact: artifact.Artifact):
        print("PosLoc")

if __name__ == "__main__":
    print("main")

    ar = artifact.ArtifactReadWrite()
    artifact = ar.reader("artifact_in/p00114")

    posloc = PosLoc("stations.dat")
    posloc.fix(artifact)

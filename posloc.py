#
# Title: posloc.py
# Description: posloc fix
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import artifact
import station

class PosLoc:
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

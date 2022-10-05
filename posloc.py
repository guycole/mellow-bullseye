#
# Title: posloc.py
# Description: posloc fix
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import math

import artifact
import gcircle as gc
import station
import utility as util


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

    def __init__(self):
        self.cv = [0, 0, 0]
        self.ebpni = []
        self.ebpnj = []
        self.ebpnk = []
        self.ebvi = []
        self.ebvj = []
        self.ebvk = []

    def xform(self, artifact: artifact.Artifact):
        """coordinate conversion"""
        for ii in artifact.observations:
            bpni = math.cos(ii.bearing.rad_val)
            bpnj = -math.sin(ii.bearing.rad_val)
            phi = util.PI_HALF - ii.location.lat.rad_val
            theta = ii.location.lng.rad_val
            cphi = -math.cos(phi)
            t11 = math.cos(theta)
            t31 = -math.sin(theta)
            t12 = cphi * (-t31)
            t22 = math.sin(phi)
            t32 = cphi * t11

            self.ebpni.append(t11 * bpni + t12 * bpnj)
            self.ebpnj.append(t22 * bpnj)
            self.ebpnk.append(t31 * bpni + t32 * bpnj)
            self.ebvi.append(t11 * (-bpnj) + t12 * bpni)
            self.ebvj.append(t22 * bpni)
            self.ebvk.append(t31 * (-bpnj) + t32 * bpni)

    def bpe(self, artifact: artifact.Artifact):
        """compute bearing plane intersections, intersection weights and fix location"""
        cvi = 0
        cvj = 0
        cvk = 0

        obz = artifact.observations

        for ii, obs1 in enumerate(obz):
            for jj in range(ii + 1, len(artifact.observations)):
                obs2 = artifact.observations[jj]
                # print(f"{ii} {obs1.station} {jj} {obs2.station}")

                wij = obs1.weight * obs2.weight

                ibpi = (self.ebpnj[ii] * self.ebpnk[jj] - self.ebpnk[ii] * self.ebpnj[jj] * wij)
                ibpj = (self.ebpnk[ii] * self.ebpni[jj] - self.ebpni[ii] * self.ebpnk[jj] * wij)
                ibpk = (self.ebpni[ii] * self.ebpnj[jj] - self.ebpnj[ii] * self.ebpni[jj] * wij)

                doti = (ibpi * self.ebvi[ii] + ibpj * self.ebvj[ii] + ibpk * self.ebvk[ii])
                dotj = (ibpi * self.ebvi[jj] + ibpj * self.ebvj[jj] + ibpk * self.ebvk[jj])

                prod = doti * dotj
                if prod < 0:
                    continue

                if doti < 0:
                    ibpi = -ibpi
                    ibpj = -ibpj
                    ibpk = -ibpk

                cvi = cvi + ibpi
                cvj = cvj + ibpj
                cvk = cvk + ibpk

        denominator = math.sqrt(cvi ** 2 + cvj ** 2 + cvk ** 2)
        self.cv[0] = cvi / denominator
        self.cv[1] = cvj / denominator
        self.cv[2] = cvk / denominator

        phi = math.asin(cvj / denominator)
        theta = math.atan(cvi / cvk)
        if cvk < 0:
            theta = theta + util.FortranFunction.sign(math.pi, cvi)

        lat = util.Latitude(phi, True)
        lng = util.Longitude(theta, True)
        artifact.ellipse_location = util.Location(lat, lng)

    def outlie(self, artifact: artifact.Artifact):
        """reject worst bearing"""

        ndx_worst = -1
        error_worst = 0
        for ii, obs in enumerate(artifact.observations):
            if obs.weight != 0:
                if obs.error > error_worst:
                    error_worst = obs.error
                    ndx_worst = ii

        if error_worst >= 3.0:
            print(f"prune outlier {obs.station}")
            artifact.observations[ndx_worst].weight = 0
            artifact.observations[ndx_worst].bearing_used = False

    def weight(self, artifact: artifact.Artifact):
        """compute the weight for each bearing"""
        foi = artifact.radio_frequency / 1e6

        for ii, obs in enumerate(artifact.observations):
            (_, distance) = gc.GreatCircle.gcdaz(obs.location, artifact.ellipse_location)
            # print(f"{ii} {obs.station} {obs.weight} {distance} {foi}")

            # sigth is standard deviation component due to antenna beamwidth
            # CDAA beamwidth is used below
            sigth = 12.367 * math.exp(-0.364 * foi)
            if foi > 9.0:
                sigth = 2.013 * math.exp(-0.0585 * foi)
            
            # sigphi is standard deviation component due to ionosphere
            # sigphi must be reduced when groundwave bearings are included in fix
            sigphi = 1.1 + 0.955 * distance.rad_val
            if distance.rad_val <= 0.0976:
                sigphi = 0.004738 / distance.rad_val**2.376

            sqerr = 0.0003046 * (sigth * sigth + sigphi)

            # use of sin(distance) as a weighting factor cause bearing from sites > 5400 NM
            # from target to appear better than bearings < 5400 NM from target.  
            # This effect is due to the cycling of the sin function 

            sin_dist = math.sin(distance.rad_val)
            obs.weight = 1 / (sin_dist * sin_dist * math.sqrt(sqerr))
          
    def fix(self, artifact: artifact.Artifact):
        print("PosLoc")

        self.xform(artifact)
        self.bpe(artifact)
        print(artifact.ellipse_location)
        nruns = 0

        while artifact.bearing_population() > 1:
            self.weight(artifact)
            self.bpe(artifact)
            print(artifact.ellipse_location)

#        phi = math.asin(self.cv[1] / math.sqrt(self.cv[0] ** 2 + self.cv[1] ** 2 + self.cv[2] ** 2))
#        theta = math.atan(self.cv[0] / self.cv[2])
#        if self.cv[2] < 0:
#            theta = theta + util.FortranFunction.sign(math.pi, self.cv[0])

#        lat3 = util.Latitude(phi, True)
#        lng3 = util.Longitude(theta, True)
#        loc3 = util.Location(lat3, lng3)
#        print(f"test {loc3}")

            self.outlie(artifact)

            nruns+=1
            if nruns > 9:
                break;

if __name__ == "__main__":
    print("main")

    ar = artifact.ArtifactReadWrite()
    artifact = ar.reader("artifact_in/p00114")

    #    posloc = PosLoc("stations.dat")
    posloc = PosLoc()
    posloc.fix(artifact)
    print(artifact)

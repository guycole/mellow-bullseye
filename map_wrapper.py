#
# Title: mapwrapper.py
# Description: map wrapper
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

import typing

import artifact
import station
import utility


class MapWrapper:
    """basemap wrapper"""

    def __init__(self, stations: station.StationManager):
        self.sm = stations

    def corner_discovery(self) -> typing.List[utility.Location]:
        lower_lat = utility.Latitude(10.0, False)
        lower_lng = utility.Longitude(-160.0, False)
        lower_loc = utility.Location(lower_lat, lower_lng)

        upper_lat = utility.Latitude(50.0, False)
        upper_lng = utility.Longitude(-110.0, False)
        upper_loc = utility.Location(upper_lat, upper_lng)

        tangent_lat = utility.Latitude(30.0, False)
        tangent_lng = utility.Longitude(-135.0, False)
        tangent_loc = utility.Location(tangent_lat, tangent_lng)

        return [lower_loc, upper_loc, tangent_loc]

    def map_wrapper(self, artifact: artifact.Artifact):
        corners = mw.corner_discovery()
        print(corners)

        #        fig = plt.figure()

        bm = Basemap(
            corners[0].lng.dd_value,
            corners[0].lat.dd_value,
            corners[1].lng.dd_value,
            corners[1].lat.dd_value,
            resolution="c",
            area_thresh=10000.0,
            projection="gnom",
            lon_0=corners[2].lng.dd_value,
            lat_0=corners[2].lat.dd_value,
        )

        bm.drawcoastlines()
        bm.fillcontinents()

        circles = np.arange(10, 90, 20)
        bm.drawparallels(circles, labels=[0, 1, 0, 0])

        meridians = np.arange(-180, 180, 30)
        bm.drawmeridians(meridians, labels=[1, 1, 0, 1])

        latz = []
        lngz = []
        for key in self.sm.stations:
            print(key)
            print(sm.get_station(key))

            xx, yy = bm(
                sm.get_station(key).location.lng.dd_value,
                sm.get_station(key).location.lat.dd_value,
            )

            plt.text(
                xx,
                yy,
                key,
                fontsize=12,
                fontweight="bold",
                ha="left",
                va="bottom",
                color="k",
            )

            latz.append(sm.get_station(key).location.lat.dd_value)
            lngz.append(sm.get_station(key).location.lng.dd_value)

        if artifact.actual_location is not None:
            print(f"actual location {artifact.actual_location}")
            latz.append(artifact.actual_location.lat.dd_value)
            lngz.append(artifact.actual_location.lng.dd_value)

        if artifact.estimated_location is not None:
            print(f"estimate location {estimated.actual_location}")
            latz.append(estimated.actual_location.lat.dd_value)
            lngz.append(estimated.actual_location.lng.dd_value)

        xx, yy = bm(lngz, latz)
        bm.scatter(xx, yy, marker="D", color="m")

        for key in self.sm.stations:
            print(key)
            print(sm.get_station(key))
            aa = sm.get_station(key)

            bm.drawgreatcircle(
                aa.location.lng.dd_value,
                aa.location.lat.dd_value,
                artifact.actual_location.lng.dd_value,
                artifact.actual_location.lat.dd_value,
                linewidth=2,
                color="b",
            )

        plt.title("Mellow Bullseye")
        plt.show()


if __name__ == "__main__":
    print("main")

    sm = station.StationManager()
    sm.read_stations("stations.dat")

    ar = artifact.ArtifactReader()
    artifact = ar.reader("artifact_in/p00114")

    mw = MapWrapper(sm)
    mw.map_wrapper(artifact)

#
# Title: gcircle.py
# Description: great circle class and methods
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import math
import typing

import utility

class GreatCircle:

    def gcrab(self, source: utility.Location, destination: utility.Location) -> typing.Tuple[float, float]:
        """calculate great circle range and bearing between two points"""

        csn1 = math.cos(source.lng.radian_value)
        snn1 = math.sin(source.lng.radian_value)

        cst1 = math.cos(source.lat.radian_value)
        snt1 = math.sin(source.lat.radian_value)

        csn2 = math.cos(destination.lng.radian_value)
        snn2 = math.sin(destination.lng.radian_value)

        cst2 = math.cos(destination.lat.radian_value)
        snt2 = math.sin(destination.lat.radian_value)

        distance = csn1*cst1*csn2*cst2+snn1*cst1*snn2*cst2+snt1*snt2
        distance = math.acos(distance)

        if distance < utility.epsilon:
            bearing = 0.0
        else:
            temp1 = -csn1*snt1*csn2*cst2-snn1*snt1*snn2*cst2+cst1*snt2
            temp2 = -snn1*csn2*cst2+csn1*snn2*cst2
            bearing = math.atan2(temp2, temp1)
            if bearing < 0.0:
                bearing=bearing+math.pi*2.0
    
        return (distance, bearing)

if __name__ == "__main__":
    print("main")


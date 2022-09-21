#
# Title: artifact_test.py
# Description: test for artifact classes
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
import pytest

import artifact
import utility

def make_observation() -> artifact.Observation:
    bearing = utility.DdAngle(123.456, False)
    return artifact.Observation('XXX', 'A', True, bearing)

def test_artifact():
    lat1 = utility.Latitude(12.3456, False)
    lng1 = utility.Longitude(123.456, False)
    loc1 = utility.Location(lat1, lng1)

    aa = artifact.Artifact('pytest')
    aa.actual_location = loc1
    aa.callsign = 'UREZ'
    aa.fix_algorithm = 'testaroo'
    aa.observations.append(make_observation())
    aa.radio_frequency = 123456
    aa.time_stamp = 87654321
 
    arw = artifact.ArtifactReadWrite()
    arw.writer("/tmp/pytest", aa)
    
    aa = arw.reader("/tmp/pytest")
    assert aa.actual_location == loc1
    assert aa.ellipse_location is None
    assert aa.callsign == 'UREZ'
    assert aa.fix_algorithm == 'testaroo'
    assert aa.id == 'pytest'
    assert len(aa.observations) == 1
    assert aa.observations[0].station == 'XXX'
    assert aa.radio_frequency == 123456
    assert aa.time_stamp == 87654321
    assert aa.version == 1
  
def test_observation():
    obs1 = make_observation()

    assert obs1.bearing_used is False
    assert obs1.id_certain is True
    assert obs1.station == 'XXX'
    assert obs1.quality == 'A'
    assert obs1.bearing == utility.DdAngle(123.456, False)

    obs2 = make_observation()
    assert obs1 == obs2

    obs2.station = 'YYY'
    assert obs1 != obs2

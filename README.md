# mellow-bullseye
Mellow Bullseye [HFDF] (https://en.wikipedia.org/wiki/Direction_finding) location demonstration.

<<<<<<< HEAD
## Introduction
How to determine transmitter location on a global scale using [HF radio](https://en.wikipedia.org/wiki/High_frequency)?  One approach would be to create a collection of stations scattered around the globe which could be tasked to monitor a radio frequency and return an observed bearing (and bearing quality).  Transmitter location could be calculated using the observed bearings.

![graphic1](https://github.com/guycole/mellow-bullseye/blob/main/early.png)

## Application/Utilities
+ autofix.py consumes files from artifact_in and writes updated files to artifact_out.
+ bullseye.py provides a UI to interactivly processs artifacts
+ generator.py creates artifacts for testing

## Conventions
+ locations in decimal degrees (no DMS) +North, +East
+ bearings are always positive, clockwise from true north
=======
Given some stations (stations.dat), read the cases (in case directory) and discover emitter location.

## Domain Classes
>>>>>>> 5f49c775a9d197aa1ea974b0e40c2b25503f2c87

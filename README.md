# mellow-bullseye
Mellow Bullseye [HFDF](https://en.wikipedia.org/wiki/Direction_finding) location demonstration.  This repository contains python ports of old HFDF fix (location estimating) routines and some applications which demonstrate their use.  Of course, the world has long since moved away from HF radio, and the stations which used to take these observations have been closed since the mid 1990s.

## Introduction
How to determine transmitter location on a global scale using [HF radio](https://en.wikipedia.org/wiki/High_frequency)?  One approach would be to create a collection of stations scattered around the globe which could be tasked to monitor a radio frequency and return an observed bearing (and bearing quality).  Transmitter location could be estimated using the observed bearings.

![graphic1](https://github.com/guycole/mellow-bullseye/blob/main/early.png)

## Application/Utilities
+ autofix.py consumes files from artifact_in and writes updated files to artifact_out.
+ bullseye.py provides a UI to interactivly processs artifacts
+ generator.py creates artifacts for testing

## Fix Algorithms
+ POSLOC

## Conventions
+ locations in decimal degrees (no DMS) +North, +East
+ bearings are always positive, clockwise from true north

## Credits
+ I am not the original author for any of these fix algorithm.  The fix algorithms here are ported from either FORTRAN or NELIAC as I have time and interest.  
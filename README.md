# mellow-bullseye
Mellow Bullseye [HFDF] (https://en.wikipedia.org/wiki/Direction_finding) location demonstration.

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

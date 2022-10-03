#!/bin/bash
#
# Title: black_all.sh
# Description: invoke black formatter
# Development Environment:OS X 12.5.1/Python 3.9.13
# Repository: https://github.com/guycole/mellow-bullseye
#
#PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
source ./venv/bin/activate
black *.py
/usr/bin/afplay /System/Library/Sounds/Submarine.aiff
#
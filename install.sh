#!/bin/bash
# Name: install.sh
#
# Copies kentrace.py to /usr/local/bin
#
# Usage: install.sh
set -e # bash should exit the script if any statement returns a non-true 
       #return value
thisdir="$PWD"

cp kentrace.py "/usr/local/bin"
echo "Copied kentrace.py to /usr/local/bin."



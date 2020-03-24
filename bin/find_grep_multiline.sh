#!/bin/bash
DIR=$1
PATTERN=$2
#find $DIR -name "*.po" -exec grep -Pzo 'fuzzy.*\n\nmsgstr' /dev/null {} \;
find $DIR -name "*.po" -exec grep -rliPzo "$PATTERN" /dev/null {} \;

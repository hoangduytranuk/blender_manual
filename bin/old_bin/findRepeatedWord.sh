#!/bin/bash
egrep -n "(\b[[:alpha:]]+) \1\b" $1

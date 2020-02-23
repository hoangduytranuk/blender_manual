#!/bin/bash
histfile=$HOME/Documents/hoang_history.txt
tempfile=$HOME/tmp.txt
history >> $histfile
cat $histfile | sort -nu > $tempfile
mv $tempfile $histfile

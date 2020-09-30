#!/usr/bin/env python3
import os
import sys
from argparse import ArgumentParser
# cat $1| awk 'BEGIN{FS="$2"} { print length, $0 }' | sort -n -s | cut -d" " -f2-
# print('this is me!!')
import fileinput

line_list = []
for lines in fileinput.input():

    line_list.append(lines.strip())

sorted_line_list = sorted(line_list, key=lambda x: len(x[0]), reverse=True)
print(sorted_line_list)

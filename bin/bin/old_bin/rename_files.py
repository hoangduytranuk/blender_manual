#!/usr/bin/env python

import fnmatch
import re
import sys
import os

__ext = ['*.htm','*.gif']

def test_one():
	for root, dirs, files in os.walk(os.getcwd(), topdown=True):
		for ext in __ext:
			for f in fnmatch.filter(files, ext):
				print os.path.join(root, f)
		break

def test_two():
	#line = "readyear.htm onestep.gif"
	line = ["readyear.htm", "one.gif"]
	for l in line:
		match = re.search(r'\.(htm|gif)$', l, re.M|re.I)
		if match:
			print 'match.group()', match.group()

	for root, dirs, files in os.walk(os.getcwd(), topdown=True):		
		for f in files: #r'*.htm'
			match = re.search(r'\.(htm|gif)$', f, re.M|re.I)
			if (match):
				print "matched:", os.path.join(root, f)
		break

test_two()

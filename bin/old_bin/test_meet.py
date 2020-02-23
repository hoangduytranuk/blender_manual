#!/usr/bin/python
a = 12
b = 18
speed=1
meet=False
range=1000
for x in xrange(0, range):
	is_div_12 = (x % a == 0)
	is_div_18 = (x % b == 0)
	meet = (is_div_12 and is_div_18)
	if (meet):
		print("meet: x = ", x)
	a+=speed
	b+=speed

if (meet):
	print ("met")
else:
	print("Did not meet")

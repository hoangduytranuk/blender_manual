#!/usr/bin/python
import math
#How many digits does this number have 1234567891011...201620172018

class exercise :
    def doit(self):
        count=0
	num_digit=0
        for a in range(1, 2018):
		if (a < 10):
			num_digit=1
		elif (a < 100):
			num_digit=2
		elif (a < 1000):
			num_digit=3
		elif (a < 10000):
			num_digit=4
		count += num_digit
#		if (a == 2017):
#			print('num_digit={}, count={}').format(num_digit, count)
        print('count is {}').format(count)


if __name__ == '__main__':	
	x = exercise()
	x.doit()


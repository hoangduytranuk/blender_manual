#!/usr/bin/python
import math
#Use distinct integers from 1 to 100 (inclusive) - [A - B] how many ways can the expression be positive but less than 10?

class exercise :
    
    def doit(self):
        count=0
        for a in range(1,100):
            for b in range(1, 100):
		if (a > b):
	                test = (a - b)
        	        valid = (test > 0 and test < 10)
			count += valid 
        print('count is {}').format(count)

	
if __name__ == '__main__':	
	x = exercise()
	x.doit()


#!/usr/bin/python
import math
#How many ordered integer (a,b,c) solutions does the equation abc = 1000 have? How quickly can you count them

class exercise :
    target=1000
    def doit(self):
	v_from=(-1*self.target)+1
	v_to=self.target-1
	result=self.target
        count=0
        for a in range(v_from, v_to):
            for b in range(v_from, v_to):
		for c in range(v_from, v_to):
	                test = (a * b * c)
        	        valid = (test == result)
			count += valid 
			if (valid):
				print("a = {}, b={}, c={}").format(a,b,c)
        print('count is {}').format(count)

	
if __name__ == '__main__':	
	x = exercise()
	x.doit()


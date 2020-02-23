#!/usr/bin/python
import math

class exercise :
    
    def doit(self):
        val = math.pow(2, 6)
        print('value is {}').format(val)
        target = val
        for i in range(7):
            target = target / val
            
        print('target is {}').format(target)
        
        d = math.pow(2,4)
        print('value is {}').format(d)
        count=0
        val = d 
        while True:
            if (val == target):
                break
            val = val / d
            count +=1
        print('count is {}').format(count)

	
if __name__ == '__main__':	
	x = exercise()
	x.doit()
	
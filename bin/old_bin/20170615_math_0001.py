#!/usr/bin/python
# coding: utf-8
#special character: Ctrl+Shift+U, hex code of char, Enter
import math
#right triangle with Ө, h: 25, opposite = 15. If move the h up, doubling Ө -> 2Ө, what is new opposite length? 

class exercise :
    def doit(self):
	#sin(Ө) = 15/25, Ө=asin(15.0/25.0) => 36.86989
	#sin(2xӨ) = x/25
	#sin(2xӨ)*25 = x
	for exp in range(1, 10):
            p = math.pow(101.0, exp)                        
            print('exp={} result={}').format(exp, p)


if __name__ == '__main__':	
	x = exercise()
	x.doit()


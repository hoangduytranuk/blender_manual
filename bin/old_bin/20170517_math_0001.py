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
	radians = math.asin(15.0/25.0)
	angle = math.degrees(radians) 
	double_angle = angle*2
	double_radians = math.radians(double_angle)
	new_opposite = math.sin(double_radians)*25.0	
        print('new_opposite is {}').format(new_opposite)


if __name__ == '__main__':	
	x = exercise()
	x.doit()


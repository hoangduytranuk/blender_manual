#!/usr/bin/python3
# coding: utf-8

def isPrime(n):
    return all(n%m for m in range(2, int(n**0.5+1)))

if __name__ == '__main__':
    list=[]
    list.append([a for a in range(1, 10**4) if isPrime(a)])
    print(list)
    print(len(list[0]))
    print(list[0])
    b=sum(list[0])
    print(b)
    
    list=[]
    list.append([a**3 for a in range(1, 7)])
    print(list)
    b=sum(list[0])
    print("sum of a**3 from (1-6)={}".format(b))
    
    list=[]
    list.append([a for a in range(1, 7)])
    print(list)
    c=sum(list[0])
    print("sum of (1-6)^2={}".format(c**2))
    

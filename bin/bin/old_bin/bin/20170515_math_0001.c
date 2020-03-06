#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

//
//	      A
//        A A
//     AA A
//+AAA A
//-------------------------------------------
//  ? ? ? ? ?


void main(void){
	int five_digits = 99999;
	for (int a = 0; a <= 9; a++){
		int aa = a*10 + a;
		int aaa = a*100 + aa;
		int aaaa = a * 1000 + aaa;
		int aaaaa = a + aa + aaa + aaaa;
		bool valid = (aaaaa <= five_digits);
		if (valid){
			printf("a=%d; result=%d\n", a, aaaaa);
		}
	}
}

#include <stdio.h>
#include<string.h>

//how many digits does this number have 1234567891011....201520162017

void main(void){
	int count, result = 0;
//	for(int i=1; i <= 2017; i++){
//		if (i < 10) count = 1; else
//		if (i < 100) count = 2; else
//		if (i < 1000) count = 3; else
//		if (i < 10000) count = 4;
//		result += count;		
//	}
	result = 2017*4 - 999 - 99 - 9 ;
	printf("result: %d\n", result);
}

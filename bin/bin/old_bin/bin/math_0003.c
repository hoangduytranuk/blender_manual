#include <stdio.h>
#include <stdbool.h>

const int TARGET=1000;

void main(void){
	int v_from=-TARGET;
	int v_to=TARGET;
	int a, b, c;
	int count=0;
	for (a=v_from; a <= v_to; a++){
	for (b=v_from; b <= v_to; b++){
	for (c=v_from; c <= v_to; c++){
		int test=(a*b*c);
		bool valid = (test == TARGET);
		if (valid){
			printf("a=%d, b=%d, c=%d\n", a, b, c);
			count++;
		}
	}
	}
	}
	printf("Number of solution is: %d\n", count);
}

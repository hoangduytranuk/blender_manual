#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

//Distinct letters represent distinct digits
//    AA
//    BB
// + CC
//---------
//  ABC
//What is ABC?

void main(void){
	for (int a = 0; a <= 9; a++){
		for (int b = 0; (b <= 9 && b != a); b++){
			for (int c = 0; (c <= 9 && c != a && c != b); c++)
			{
				int aa = a * 10 + a;
				int bb = b * 10 + b;
				int cc = c * 10 + c;
				int sum = aa + bb + cc;
				int target = a * 100 + b * 10 + c;

				printf("aa =%02d; bb = %02d; cc = %02d; sum=%d; target=%d\n", aa, bb, cc, sum, target);

			}
		}
	}
}

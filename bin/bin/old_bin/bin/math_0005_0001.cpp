#include <iostream>
#include <string>

//Distinct letters represent distinct digits
//    AA
//    BB
// + CC
//---------
//  ABC
//What is ABC?

using namespace std;

class example{
	private:
		int a, b, c;
	public:
		int res;
		int target;
		void sayHello(void);
		void doCalc(void);
};

void example::sayHello(void){
	string str = "Hello World" ;
	cout << str << endl;
}

void example::doCalc(void){
	for(a = 0; a <= 9; a++){
		for(b = 0; b <= 9 && b != a; b++){
			for(c = 0; c <= 9 && c != a && c != b; c++){
				int aa = a*10 + a;
				int bb = b*10 + b;
				int cc = c*10 + c;
				int sum = aa + bb + cc;
				int target = a * 100 + b * 10  + c;
				cout << "aa=" << aa << " bb=" << bb << " cc=" << cc << " sum= " << sum << " target=" << target << endl;
				if (sum == target){
					cout << "FOUND" << endl;
				}
			}
		}
	}
}

int main(){
	example ex;
	ex.doCalc();
	return 0;
}

// Author: Christopher Coyle
// cite: Class Notes
//cite: http://www.mathopenref.com/polygonradius.html
// cite: http://www.cplusplus.com/reference/cmath/sin/

//HW1b Convergence of n-gons

#include <cmath>
#include <iostream>
using namespace std;

int main() {

	cout << "Hello User" << endl;

	const double PI = 3.1515926535897;
	double r = 1.0;
	unsigned int n = 1;

	while (n <= (1000000 - 1)) {

		n++;
		r = 1 / (2 * (sin(PI / n)));

		if (n == 10) {
			cout << "number of sides: " << n << endl;
			cout << "radius: " << r << '\n' << '\n';
		}

		else if (n == 100) {
			cout << "number of sides: " << n << endl;
			cout << "radius: " << r << '\n' << '\n';
		}

		else if (n == 1000) {
			cout << "number of sides: " << n << endl;
			cout << "radius: " << r << '\n' << '\n';
		}

		else if (n == 10000) {
			cout << "number of sides: " << n << endl;
			cout << "radius: " << r << '\n' << '\n';
		}

		else if (n == 100000) {
			cout << "number of sides: " << n << endl;
			cout << "radius: " << r << '\n' << '\n';
		}

		else if (n == 1000000) {

			cout << "number of sides: " << n << endl;

			cout << "radius: " << r << '\n' << '\n';

		}
	}

	/*
	 cout << "number of sides: " << endl;
	 cout << n << endl;

	 cout << "radius: " << endl;
	 cout << r <<  endl;
	 */
	cout << "Bye User" << endl;

}

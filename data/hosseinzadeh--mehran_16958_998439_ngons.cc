 //Author Mehran Hosseinzadeh
//Convergence of n-gons
//Yifei Cai helped me to this works
#include <iostream>
#include <cmath>

using namespace std;
float pi = 3.14159
float radius(int n){
	float r = 1;
	float R;
	for(int i=3;i<=n;i++){
		R = r / cos(pi/i);
		r = R;
	}
	return R;
}


int main(){
	cout << "Radius= "<< radius(10) << " for n= 10 \n";
	cout << "Radius= "<< radius(100) << " for n= 100 \n";
	cout << "Radius= "<< radius(1000) << " for n= 1000 \n";
	cout << "Radius= "<< radius(10000) << " for n= 10000 \n";
	cout << "Radius= "<< radius(100000) << " for n= 100000 \n";
	cout << "Radius= "<< radius(1000000) << " for n= 1000000 \n";

}


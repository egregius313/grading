//
//  main.cpp
//  HW1-Convergence of n-gons
//
//  Created by songnan on 15/9/3.
//  Copyright (c) 2015年 songnan. All rights reserved.
//

#include <iostream>
#include <iomanip>
#include <cmath>
using namespace std;
int main() {
    double ngons(int n);
    for(int n=10;n<=pow(10,6);n=10*n){
     cout << "n=" << n <<'\t'<< "r="<< ngons(n)<<endl;
    }
    return 0;
}
double ngons(int n){
    const double PI = 3.14159265358979;
    double r=1;//Start with a circle r= 1
    for(int x=3;x<=n;x++){
        double t=(x-2)*PI/x; //The angle of the n-gons
        r=r/sin(t/2);
    }
    return r;
}

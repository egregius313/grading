#include <iostream>

using namespace std;

int main()
{
    float sum1_float, sum2_float = 0;
    double sum1_double, sum2_double = 0;

    for(int a = 1; a <= 100; a++) {
        sum1_float += 1/(float)a;
        sum1_double += 1/(double)a;
    }

    for(int a = 100; a > 0; a--) {
        sum2_float += 1/(float)a;
        sum2_double += 1/(double)a;
    }
    float diff_float = sum1_float - sum2_float;
    double diff_double = sum1_double - sum2_double;

    cout << "float sum1: " << sum1_float << " | float sum2: " << sum2_float << endl;
    cout << "float diff: " << diff_float << endl;
    cout << "double sum1: " << sum1_double << " | double sum2: " << sum2_double << endl;
    cout << "double diff: " << diff_double << endl;

    return 0;
}

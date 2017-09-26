#include <iostream>

using namespace std;
void collatz(int);

int main()
{
    int n = 0;
    cout << "Enter a number: ";
    cin >> n;
    collatz(n);

    return 0;
}

void collatz(int n) {
    if (n == 1) cout << endl;
    else {
        if (n % 2 == 1) n = 3*n + 1;
        else n = n/2;
        cout << n << ", ";
        collatz(n);
    }
}

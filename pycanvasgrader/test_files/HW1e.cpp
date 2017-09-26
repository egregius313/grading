#include <iostream>

using namespace std;

int fact(int);

int main()
{
    int n = 0;
    cout << "Enter a number: ";
    cin >> n;
    cout << fact(n);

    return 0;
}

int fact(int n) {
    int total = 1;
    while (n > 0)
        total *= n--;
    return total;
}

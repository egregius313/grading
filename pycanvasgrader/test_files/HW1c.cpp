#include <iostream>

using namespace std;

int sum(int);
int sum2(int);

int main()
{
    cout << sum(100) << '\n';
    cout << sum2(100) << '\n';
    return 0;
}

int sum(int n) {
    int total = 0;
    for (int a = 1; a <= n; a++)
        total += a;

    return total;
}

int sum2(int n) {
    return n * (n + 1) / 2;
}

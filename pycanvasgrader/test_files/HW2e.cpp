#include <iostream>

using namespace std;

int fact(int);
int fibo(int);
unsigned choose(unsigned, unsigned);

int main()
{
    cout << fact(5) << ' ' << fact(5) << '\n';
    cout << fact(15) << ' ' << fact(15) << '\n';
    cout << fibo(5) << ' ' << fibo(5) << '\n';
    cout << fibo(13) << ' ' << fibo(13) << '\n';
    cout << choose(52,6) << '\n';

    return 0;
}

unsigned choose( unsigned n, unsigned k )
{
    if (k > n) return 0;
    if (k * 2 > n) k = n-k;
    if (k == 0) return 1;

    int result = n;
    for( int i = 2; i <= k; ++i ) {
        result *= (n-i+1);
        result /= i;
    }
    return result;
}

int fibo(int n)
{
   if (n <= 1)
      return n;
   return fibo(n-1) + fibo(n-2);
}

int fact(int n)
{
    if(n > 1)
        return n * fact(n - 1);
    else
        return 1;
}

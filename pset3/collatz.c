#include <stdio.h>
#include <stdlib.h>

int collatz(int n);
int test(int n);
int i;

int main(void)
{
    // collatz(27);
    test(2);
    printf("%i\n", i);
}

int collatz(int n)
{
    if(n == 1)
    {
        return 0;
    }
    else if ((n % 2) == 0)
    {
        i++;
        return 1 + collatz(n / 2);

    } else {
        i++;
        return 1 + collatz((3 * n) + 1);
    }
}

int test(int n)
{
    if (n == 20)
    {
        return 0;
    } else {
        i++;
        return 1 + test(n + 1);
    }
}
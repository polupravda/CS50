#include <cs50.h>
#include <stdio.h>
#include <crypt.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

char strSalt[] = "q1c";
//char strSalt[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

int main(void)
{
    string typedPass = get_string("Type your pass: \n");
    time_t t;
    srand((unsigned)time(&t));

    char arr[3];

    for (int i = 0; i < 2; i++)
    {
	    arr[i] = strSalt[rand() % 3];
    }
    arr[2] = '\0';

    char *cryptedData = crypt(typedPass, arr);
    printf("Your password hash: %s\n", cryptedData);
}


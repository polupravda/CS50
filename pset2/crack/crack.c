// q1vo6MP0/Yt46

#include <cs50.h>
#include <stdio.h>
#include <crypt.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

int compare(const void *a, const void *b);
void allLexicographicRecur (char *str, char *data, int last, int index);
void allLexicographic(char *str, int a);
void check(const char *str1, const char *str2, const char *str3);

// test data
// char strAlpha[] = "abcd";
// char strSalt[] = "q1c";
// const int maxLength = 3;

char strAlpha[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
char strSalt[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
const int maxLength = 5;

const int saltLength = 2;
char *passHash;

// Represents a node in a liked list
typedef struct node
{
    char value[saltLength + 1];
    struct node *next;
}
node;

int main(int argc, string argv[])
{
    // check if the user has entered pass hash
    if (argc != 2)
    {
        printf("Error: enter password hash\n");
        return 1;
        void exit(int status);
    }

    passHash = argv[1];

    for (int j = 1; j <= maxLength; j++)
    {
        allLexicographic(strAlpha, j);
    }

    return 0;
}

void allLexicographicRecur (char *str, char *data, int last, int index)
{
    int i, len = strlen(str);

    for (i = 0; i < len; i++)
    {
        data[index] = str[i];

        if(index == last)
        {
            char a = passHash[0];
            char b = passHash[1];
            char *saltT = (char *) malloc(sizeof(char) * (saltLength + 1));
            saltT[0] = a;
            saltT[1] = b;
            saltT[saltLength] = '\0';
            const char *salt = saltT;

            char *cryptedData = crypt(data, salt);
            check(cryptedData, passHash, data);

            free(saltT);
        }
        else
            allLexicographicRecur(str, data, last, index + 1);
    }
}

// create all possible alphalexical passwords of size 1-5 characters
void allLexicographic(char *str, int a)
{
    int len = a;

    char *data = (char *) malloc(sizeof(char) * (len + 1));
    data[len] = '\0';

    qsort(str, len, sizeof(char), compare);

    allLexicographicRecur(str, data, len - 1, 0);

    free(data);
}

int compare(const void *a, const void *b)
{
    return (*(char *)a - *(char *)b);
}

// check if given pass hash matches and prints the found password
void check(const char *str1, const char *str2, const char *str3)
{
    if (strcmp(str1, str2) == 0)
    {
        printf("\n\nFound! Password is: %s\n\n\n", str3);
        exit(0);
    } else {
        printf("%s | %s\n", str1, str2);
        //printf(" \n");
    }
}
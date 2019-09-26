#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    int n = atoi(argv[1]);

    for (int ii = 0; ii < 3; ii++) // imitates looping through rows of a small bmp
    {
        for(int p = 0; p < n; p++)
        {
            for (int j = 0; j < 3; j++) // imitates looping through every pixel in a row of a small bmp
            {
                for(int k = 0; k < n; k++)
                {
                    printf("#"); // 3 px multiplied
                }
            }
            printf("-");
            printf("\n");
        }
    }
}
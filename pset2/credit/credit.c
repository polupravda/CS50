#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// 4003600000000014

long input;
int inputDigitCount = 0;

int main(void) {
    do {
        input = get_long("Number: ");
    } while (input < 0);

    // initialise a counter for totatl digits num of the input
    long a = input;

    while (a)
    {
        a = a/10;
        inputDigitCount++;
    }

    // create an array of the input length: direct & inverted
    int inputDir[inputDigitCount];
    int inputRvrs[inputDigitCount];

    long b = input;
    for (int i = 0; i < inputDigitCount; i++)
    {
        inputRvrs[i] = b % 10;
        b /= 10;
    }

    long c = input;
    int inputDirCount = inputDigitCount;

    for (int i = inputDirCount; i > 0; i--)
    {
        inputDir[(i - 1)] = c % 10;
        c /= 10;
    }

    // find out how long the new arrays will be
    int arrSecDigFromEndLen = inputDigitCount / 2;

    int sumFrstDigFromEnd = 0;
    int sumSecDigFromEnd = 0;

    int sumTotal = 0;

    // loop over the inputRvrs arr and separate digits into 2 new arrays
    for (int k = 0, l = 0, numOfItr = (arrSecDigFromEndLen * 2); k < numOfItr; l++, k = k + 2)
    {
        // digits starting from 2nd from the end
        // multiply each by 2
        // add those products’ digits

        int digit = 0;
        int digitT = 0;
        int breakDown = (inputRvrs[k + 1]) * 2;

        if (breakDown > 9) {
            digitT = breakDown % 10;
            digit = digitT + 1;
            breakDown /= 10;
        } else
        {
            digit = breakDown;
        }

        sumSecDigFromEnd += digit;
    }

    for (int k = 0, l = 0; k < inputDigitCount; l++, k = k + 2)
    {
        // calculate the sum of every 2nd digit starting from the 1st digit of arr
        sumFrstDigFromEnd += inputRvrs[k];
    }

    sumTotal = sumFrstDigFromEnd + sumSecDigFromEnd;

    if (sumTotal % 10 == 0)
    {
        // AMEX\n 34 or 37; 15-digit;
        if (inputDigitCount == 15 && inputDir[0] == 3 && (inputDir[1] == 4 || inputDir[1] == 7))
        {
            printf("AMEX\n");
        } else if (inputDigitCount == 16 && inputDir[0] == 5 && (inputDir[1] == 1 || inputDir[1] == 2 || inputDir[1] == 3 || inputDir[1] == 4 || inputDir[1] == 5))
        {
            // MASTERCARD\n 51, 52, 53, 54, or 55; 16-digit;
            printf("MASTERCARD\n");
        } else if ((inputDigitCount == 13 || inputDigitCount == 16) && inputDir[0] == 4)
        { // VISA\n 4; 13- and 16-digit;
            printf("VISA\n");
        } else {
            printf("INVALID\n");
        }
    } else
    {
        printf("INVALID\n");
    }
    printf("%i %i\n", sumFrstDigFromEnd, sumSecDigFromEnd);

        // 4003600000000014
        // arrSecDigFromEnd:  40600001
        // arrFrstDigFromEnd: 03000004

        // 40036000000000149
        // arrSecDigFromEnd:  03000004
        // arrFrstDigFromEnd: 406000019

        // 40036000000000189
        // arrSecDigFromEnd:  03000008 // 6 + (1 + 6) = 13
        // arrFrstDigFromEnd: 406000019 // 20
}
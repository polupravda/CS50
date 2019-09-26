#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(void)
{
    int arr[] = {0, 1, 2, 3, 2, 3, 0, 9, 8, 2, 3, 0, 9, 8, 2, 3};

    for(int startPos = 0, arrLength = (sizeof arr / sizeof *arr); startPos < arrLength; startPos++)
    {
        //printf("%i\n", arr[i]);
        // check if there is a repeating sequence here:

        for(int sequenceLength = 1; sequenceLength <= (arrLength - startPos) / 2; sequenceLength++) // check of "2" needed
        {
            bool sequencesAreEqual = true;
            for(int i = 0; i < sequenceLength; i++)
            {
                if(arr[startPos + i] != arr[startPos + sequenceLength + i])
                {
                    sequencesAreEqual = false;
                    break;
                }
                if(sequencesAreEqual)
                {
                    printf("Found repeating sequence at pos %i\n", startPos);
                }
            }
        }
    }
}
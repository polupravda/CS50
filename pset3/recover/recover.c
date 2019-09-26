#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if(argc != 2)
    {
        fprintf(stderr, "Usage: ./recover fliname\n");
        return 1;
    }

    char *infile = argv[1];
    char *outfile;
    int b = 512;

    // open card file
    FILE *inptr = fopen(infile, "r");

    // check if the file can be opened
    if(inptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Can not open %s\n", infile);
        return 2;
    }

    // create a buffer var
    unsigned char buffer[b];
    int imgCount = 0;
    FILE *img;

    // find out the length of the input file
    fseek(inptr, 0L, SEEK_END);
    int inptrLength = ftell(inptr);
    fseek(inptr, 0L, SEEK_SET);

    // repeat until end of card
    for(int i = 0, l = (inptrLength / b); i < l; i++)
    {

        // read 512 B into a buffer from inptr
        fread(&buffer, b, 1, inptr);

        // start of a new jpg?
        if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            char filename[7];
            sprintf(filename, "%03i.jpg", imgCount);
            img = fopen(filename, "w");

            do {
                fwrite(&buffer, b, 1, img);

                int check = fread(&buffer, 1, b, inptr);

                if(check < b)
                {
                    break;
                }
            } while(!(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0));

            // move "cursor" 512 B back to clear the buffer from the starting bytes of the next image
            fseek(inptr, -b, SEEK_CUR);

            // set next image name index
            imgCount++;

        }
    }

    // close any remaining files
    fclose(inptr);

    fclose(img);

    return 0;
}

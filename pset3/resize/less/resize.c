// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        printf("Usage: resize n infile outfile\n");
        return 1;
    }

    // remember filenames
    int n = atoi(argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];

    if(n < 0 || n > 100) {
        printf("Positive number less than 100\n");
        return 1;
    }

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        printf("Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        printf("Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        printf("Unsupported file format.\n");
        return 4;
    }

    // redefine variables for values in BITMAPINFOHEADER
    int biWidthOld = bi.biWidth;
    int biWidthNew = biWidthOld * n;

    int biHeightOld = bi.biHeight;
    int biHeightNew = biHeightOld * n;

    // determine padding for scanlines
    int paddingOld = (4 - (biWidthOld * sizeof(RGBTRIPLE)) % 4) % 4;
    int paddingNew = (4 - (biWidthNew * sizeof(RGBTRIPLE)) % 4) % 4;

    int biSizeImageOld = bi.biSizeImage;
    int biSizeImageNew = ((sizeof(RGBTRIPLE) * biWidthNew) + paddingNew) * abs(biHeightNew);

    // redefine variables for values in BITMAPFILEHEADER
    int bfSizeNew = biSizeImageNew + 54;

    // reconfigure values to be written into an output file
    bi.biWidth = biWidthNew;
    bi.biHeight = biHeightNew;
    bi.biSizeImage = biSizeImageNew;
    bf.bfSize = bfSizeNew;

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines - for each row (of 3)
    for (int i = 0, biHeight = abs(biHeightOld); i < biHeight; i++)
    {

        // temporary array
        RGBTRIPLE arr[biWidthNew];

        // resize horizontally
        // iterate over pixels in scanline - for each pixel in a row (of 3)
        for (int j = 0; j < biWidthOld; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            // write this triple into the outfile n times
            for (int y = 0; y < n; y++)
            {
                arr[(n * j) + y] = triple;
            }
        }

        for(int l = 0; l < n; l++)
        {

            fwrite(arr, sizeof(RGBTRIPLE), biWidthNew, outptr);

            // add new padding
            for (int k = 0; k < paddingNew; k++)
            {
                fputc(0x00, outptr);
            }
        }

        // skip over padding, if any
        fseek(inptr, paddingOld, SEEK_CUR);

        // ----- end of resize horizontally
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}

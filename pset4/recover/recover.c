#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int chunkSize = 512;
int fileNum = 0;
char *filename;

long file_size(FILE *file);
bool is_jpg(BYTE *header);

int main(int argc, char *argv[])
{

    if (argc > 2)
    {
        printf("Usage: ./recover image");
        return 1;
    }

    FILE *rawPtr = fopen(argv[1], "r");
    if (rawPtr == NULL)
    {
        printf("Could not open file \"%s\"", argv[1]);
        return 1;
    }

    long rawSize = file_size(rawPtr);
    BYTE *rawChunk = malloc(chunkSize);
    bool writing = false;
    FILE *img = NULL;
    filename = malloc(8);

    while (!feof(rawPtr))
    {
        fread(rawChunk, chunkSize, 1, rawPtr);
        bool isJpg = is_jpg(rawChunk);

        if (isJpg)
        {
            if (writing)
            {
                fclose(img);
            }
            sprintf(filename, "%03i.jpg", fileNum);
            fileNum++;
            img = fopen(filename, "w");
            writing = true;
        }

        if (writing)
        {
            fwrite(rawChunk, chunkSize, 1, img);
        }
    }

    fclose(img);
    fclose(rawPtr);

    free(rawChunk);
    free(filename);
    return 0;
}

long file_size(FILE *file)
{
    fseek(file, 0, SEEK_END);
    long fileSize = ftell(file);
    fseek(file, 0, SEEK_SET);
    return fileSize;
}

bool is_jpg(BYTE *header)
{
    if (header[0] == 255 && header[1] == 216 && header[2] == 255)
    {
        return true;
    }
    return false;
}
#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int size = 0;
    do
    {
        size = get_int("Height: ");
    }
    while (!(size > 0 && size < 9));


    for (int i = 1; i <= size; i++)
    {
        for (int j = size; j > 0; j--)
        {
            if (j <= i)
            {
                printf("#");
            }
            else
            {
                printf(" ");
            }
        }
        printf("\n");
    }
}
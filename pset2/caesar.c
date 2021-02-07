#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int isNumber(string text);
int rotate(int n, int t, int min, int max);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Error");
        return 1;
    }

    int key = 1;
    int isNumbers = isNumber(argv[1]);
    if (isNumbers)
    {
        key = atoi(argv[1]);
    }
    else
    {
        printf("Error");
        return 1;
    }


    string text = get_string("plaintext: ");
    //int textLength = strlen(text);
    //char cypher[textLength];

    //65-90 A-Z
    //97-122 a-z
    // cypher = (plain + key) % 26
    printf("ciphertext: ");
    for (int i = 0; text[i] != '\0'; i++)
    {
        int plain = (int)text[i];
        int cypher = 0;
        if (plain >= 65 && plain <= 90)
        {
            cypher = rotate(plain, key, 65, 90);
        }
        else if (plain >= 97 && plain <= 122)
        {
            cypher = rotate(plain, key, 97, 122);
        }
        printf("%c", cypher);
    }
    printf("\n");
}

int isNumber(string text)
{
    char actual = '\0';
    int i = 0;
    do
    {
        actual = text[i];
        if (!isdigit(actual))
        {
            return 0;
        }
        else
        {
            i++;
            actual = text[i];
        }
    }
    while (actual != '\0');
    return 1;
}

int rotate(int n, int t, int min, int max)
{
    int result = n + (t % n);
    if (result > max)
    {
        return (min - 1) + (result % max);
    }
    return result;
}